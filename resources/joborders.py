from flask_restful import Resource, reqparse
from models.joborders import JobOrderModel
from models.brands import BrandModel
from flask_jwt import jwt_required


class JobOrder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "technician_name", required=True, type=str, help="Technician name is required"
    )
    parser.add_argument("item", type=str, required=True, help="Item is required")
    parser.add_argument(
        "job_description", type=str, required=True, help="Job Description is required"
    )
    parser.add_argument(
        "brand_id", type=int, required=True, help="Brand ID is required"
    )

    @jwt_required()
    def get(self, _id):
        job_order = JobOrderModel.find_by_id(_id)

        if job_order:
            return job_order.json()

        return {"message": "Job Order not found."}, 404

    @jwt_required()
    def post(self, _id):
        if JobOrderModel.find_by_id(_id):
            return {
                "message": "A Job Order with id '{}' already exists.".format(_id)
            }, 400

        if not str(_id).startswith("JO") and len(_id) != 9:
            return {"message": "The job order {} is invalid.".format(_id)}, 400

        data = JobOrder.parser.parse_args()

        job_order = JobOrderModel(_id, **data)

        brand = BrandModel.find_by_id(data["brand_id"])

        if not brand:
            return {
                "message": "The Brand ID {} is not found.".format(data["brand_id"])
            }, 400

        try:
            job_order.save_to_db()
        except Exception:
            return {"message": "An error occured while adding the job order."}, 500

        return job_order.json(), 201

    @jwt_required()
    def delete(self, _id):
        job_order = JobOrderModel.find_by_id(_id)

        if job_order:
            job_order.delete_from_db()

            return {"message": "Job order deleted."}

    @jwt_required()
    def put(self, _id):
        data = JobOrder.parser.parse_args()

        job_order = JobOrderModel.find_by_id(_id)

        if job_order is None:
            data = JobOrder.parser.parse_args()

            brand = BrandModel.find_by_id(data["brand_id"])

            if not brand:
                return {
                    "message": "The Brand ID {} is not found.".format(data["brand_id"])
                }, 400
            try:
                job_order = JobOrderModel(_id, **data)
            except Exception:
                return {"message": "An error occured while adding the job order."}, 500
        else:
            job_order.technician_name = data["technician_name"]
            job_order.item = data["item"]
            job_order.job_description = data["job_description"]
            job_order.brand_id = data["brand_id"]

        job_order.save_to_db()

        return job_order.json()


class JobOrderList(Resource):
    @jwt_required()
    def get(self):
        return {
            "job_orders": [job_order.json() for job_order in JobOrderModel.query.all()]
        }


class UUID(Resource):
    @jwt_required()
    def get(self):
        job_order = JobOrderModel.query.order_by(JobOrderModel.id.desc()).first()
        uuid = "JO0000001"

        if job_order:
            temp = int(job_order.id[2:]) + 1
            uuid = "JO{}".format(str(temp).zfill(6))

        return {"uuid": uuid}
