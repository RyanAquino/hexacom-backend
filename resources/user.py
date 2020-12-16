from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_raw_jwt,
    get_jwt_identity,
)
from werkzeug.security import safe_str_cmp

from models.user import UserModel
from models.blacklist import Blacklist

from resources.jwt_custom_decorators import admin_required


class User(Resource):
    @jwt_required
    def get(self, username):
        current_user = UserModel.find_by_username(get_jwt_identity())

        if current_user.type.value == "user" and current_user.username != username:
            return {"message": "User is not allowed to view other users."}, 401

        user = UserModel.find_by_username(username)

        if user:
            return user.json()

        return {"message": "User not found."}, 404

    @admin_required
    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            try:
                user.deactivate()
            except Exception:
                return {"message": "An error occured when deactivating account."}

        return {"message": "User has been deactivated."}

    @admin_required
    def put(self, username):
        user = UserModel.find_by_username(username)
        if user:
            try:
                user.deactivate()
            except Exception:
                return {"message": "An error occured when activating account."}

        return {"message": "User has been activated."}


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field can't be blank."
    )
    parser.add_argument(
        "name", type=str, required=True, help="This field can't be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field can't be blank."
    )
    parser.add_argument(
        "number", type=str, required=True, help="This field can't be blank."
    )
    parser.add_argument(
        "address", type=str, required=True, help="This field can't be blank."
    )
    parser.add_argument(
        "status", type=str, required=True, help="This field can't be blank."
    )
    parser.add_argument(
        "type", type=str, required=True, help="This field can't be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserList(Resource):
    @admin_required
    def get(self):
        current_user = UserModel.find_by_username(get_jwt_identity())
        return {"user": [user.json() for user in UserModel.query.all() if user.username != current_user.username]}


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field can't be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field can't be blank."
    )

    def post(self):
        data = Login.parser.parse_args()
        user = UserModel.find_by_username(data["username"])

        if user.status.value != "active":
            return {
                "message": "This account has been deactivated. Please contact your administrator."
            }, 401

        if user and safe_str_cmp(user.password, data["password"]):
            return {"access_token": create_access_token(identity=user.username)}
        else:
            return {"message": "Invalid credentials."}, 401


class Logout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        blacklist = Blacklist(jti)
        print(Blacklist.verify_token(jti))
        blacklist.add()
        return {"message": "Successfully logged out"}
