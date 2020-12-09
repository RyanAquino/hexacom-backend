from db import db
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from security import authenticate, identity

from resources.joborders import JobOrder, JobOrderList, UUID
from resources.user import UserRegister

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db" Change when no Docker
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin@db/hexacom"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config['JWT_AUTH_URL_RULE'] = '/login' # IF we want to change authentication endpooint

# Set to 8 hours, change the duration of the token
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=8)

api = Api(app)
jwt = JWT(app, authenticate, identity)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(JobOrder, "/job_order/<string:id>")
api.add_resource(JobOrderList, "/job_orders")
api.add_resource(UUID, "/job_order/generate_uid")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    db.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
