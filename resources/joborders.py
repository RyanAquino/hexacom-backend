from flask_restful import Resource, reqparse
from models.joborders import JobOrderModel
from models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity


class JobOrder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("item", type=str)
    parser.add_argument("job_description", type=str)
    parser.add_argument("brand_name", type=str)

    @jwt_required
    def get(self, _id):
        """
        Get a job order using an id.

        :param _id: string
        :return: a job order in json format
        """
        job_order = JobOrderModel.find_by_id(_id)

        if job_order:
            return job_order.json()

        return {"message": "Job Order not found."}, 404

    @jwt_required
    def post(self, _id):
        """
        Create a job order

        :param _id: string
        :return: the newly created job order.
        """
        if JobOrderModel.find_by_id(_id):
            return {
                "message": "A Job Order with id '{}' already exists.".format(_id)
            }, 400

        if not str(_id).startswith("JO") and len(_id) != 9:
            return {"message": "The job order {} is invalid.".format(_id)}, 400

        data = JobOrder.parser.parse_args()
        user = UserModel.find_by_username(get_jwt_identity())

        try:
            job_order = JobOrderModel(_id, **data, technician_id=user.id)
            job_order.save_to_db()
        except Exception as e:
            print(e)
            return {"message": "An error occured while adding the job order."}, 500

        return job_order.json(), 201

    @jwt_required
    def delete(self, _id):
        """
        Delete a job order.

        :param _id: string
        """
        job_order = JobOrderModel.find_by_id(_id)

        if job_order:
            job_order.delete_from_db()

        return {"message": "Job order deleted."}


class JobOrderList(Resource):
    @jwt_required
    def get(self):
        """
        Return a list of job orders.

        :return: job order list
        """
        user = UserModel.find_by_username(get_jwt_identity())

        if user.type.value == "admin":
            data = [job_order.json() for job_order in JobOrderModel.query.all()]
        else:
            data = user.json()["job_orders"]
        return {"job_orders": data}


class UUID(Resource):
    @jwt_required
    def get(self):
        """
        Generate a job order ID

        :return: generated job order id string
        """
        job_order = JobOrderModel.query.order_by(JobOrderModel.id.desc()).first()
        uuid = "JO0000001"

        if job_order:
            temp = int(job_order.id[2:]) + 1
            uuid = "JO{}".format(str(temp).zfill(7))

        return {"uuid": uuid}


class Release(Resource):
    def post(self, _id):
        """
        Release an item in a job order.

        :param _id: string
        """
        job_order = JobOrderModel.find_by_id(_id)

        if not job_order:
            return {"message": f"Job Order with {_id} not found."}

        job_order.update_release_date()

        return {"message": "Item released."}
