from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt import jwt_required
from sqlalchemy import exc


class User(Resource):
    def get(self, username):
        user = UserModel.find_by_username(username)

        if user:
            return user.json()

        return {"message": "User not found."}, 404

    @jwt_required()
    def delete(self, name):
        brand = UserModel.find_by_name(name)

        if brand:
            try:
                brand.delete_from_db()
            except exc.IntegrityError:
                return {
                    "message": "User can't be deleted. It is associated with a job order. "
                }

        return {"message": "Brand deleted."}


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

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserList(Resource):
    @jwt_required()
    def get(self):
        return {"user": [user.json() for user in UserModel.query.all()]}
