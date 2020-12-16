from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import os
from datetime import timedelta
from db import db

from resources.joborders import JobOrder, JobOrderList, UUID, Release

# from resources.brands import Brand, BrandList
from resources.user import UserRegister, UserList, User, Login, Logout

from cli_functions.admin import admin_bp
from cli_functions.seeder import seeder_bp

from models.blacklist import Blacklist

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    os.environ.get("DB_URI") or "mysql+pymysql://root:admin@127.0.0.1/hexacom"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=8)
app.config["JWT_SECRET_KEY"] = "super-secret"

api = Api(app)
jwt = JWTManager(app)
db.init_app(app)
CORS(app, supports_credentials=True)


@app.before_first_request
def init_db():
    db.create_all()


SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.yaml"
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Hexacom-Python-Flask-REST"}
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
app.register_blueprint(admin_bp)
app.register_blueprint(seeder_bp)

api.add_resource(JobOrder, "/job_order/<string:_id>")
api.add_resource(JobOrderList, "/job_orders")
# api.add_resource(Brand, "/brand/<string:name>")
# api.add_resource(BrandList, "/brands")
api.add_resource(UUID, "/job_order/generate_uid")
api.add_resource(Release, "/release/<string:_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserList, "/users")
api.add_resource(User, "/user/<string:username>")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return Blacklist.verify_token(jti)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
