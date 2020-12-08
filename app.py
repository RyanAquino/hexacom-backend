from db import db
from flask import Flask
from flask_restful import Api

from resources.joborders import JobOrder, JobOrderList, UUID

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(JobOrder, "/job_order/<string:id>")
api.add_resource(JobOrderList, "/job_orders")
api.add_resource(UUID, "/job_order/generate_uid")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
