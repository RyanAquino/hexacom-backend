from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import UserModel


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = UserModel.find_by_username(get_jwt_identity())

        if user.type.value == "user":
            print("test")
            return {"message": "User is not allowed."}, 401
        else:
            return fn(*args, **kwargs)

    return wrapper
