from flask_restful import Resource, reqparse
from models.joborders import JobOrderModel


class JobOrder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("technician_name", type=str)
    parser.add_argument("item", type=str)
    parser.add_argument("job_description", type=str)

    def get(self, id):
        job_order = JobOrderModel.find_by_id(id)

        if job_order:
            return job_order.json()

        return {"message": "Job Order not found."}, 404

    def post(self, id):
        if not str(id).startswith("JO") and len(id) != 9:
            return {"message": "The job order is invalid.".format(id)}, 400

        if JobOrderModel.find_by_id(id):
            return {
                "message": "A Job Order with id '{}' already exists.".format(id)
            }, 400

        data = JobOrder.parser.parse_args()
        job_order = JobOrderModel(id, **data)

        try:
            job_order.save_to_db()
        except:
            return {"message": "An error occured while adding the job order."}, 500

        return job_order.json(), 201

    def delete(self, id):
        job_order = JobOrderModel.find_by_id(id)

        if job_order:
            job_order.delete_from_db()

            return {"message": "Job order deleted."}
        else:
            return {
                "message": "A Job Order with id '{}' already exists.".format(id)
            }, 400

    def put(self, id):
        data = JobOrder.parser.parse_args()

        job_order = JobOrderModel.find_by_id(id)

        if job_order is None:
            try:
                job_order = JobOrderModel(id, **data)
            except:
                return {"message": "An error occured while adding the job order."}, 500
        else:
            job_order.technician_name = data["technician_name"]
            job_order.item = data["item"]
            job_order.job_description = data["job_description"]

        job_order.save_to_db()

        return job_order.json()


class JobOrderList(Resource):
    def get(self):
        return {
            "job_orders": [job_order.json() for job_order in JobOrderModel.query.all()]
        }


class UUID(Resource):
    def get(self):
        job_order = JobOrderModel.query.order_by(JobOrderModel.id.desc()).first()
        uuid = "JO0000001"

        if job_order:
            temp = int(job_order.id[2:]) + 1
            uuid = "JO{}".format(str(temp).zfill(6))

        return {"uuid": uuid}
