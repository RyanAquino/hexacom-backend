from flask import Blueprint
from getpass import getpass
from werkzeug.security import safe_str_cmp
from flask_migrate import upgrade
from db import db

from models.user import UserModel

admin_bp = Blueprint("admin", __name__)


@admin_bp.cli.command("db_init")
def initialize_database():
    """Initialize the database and upgrde. """
    db.create_all()
    upgrade()
    print("Done.")


@admin_bp.cli.command("db_drop")
def db_drop():
    """Drop the database. """
    db.drop_all()
    print("Database dropped!")


@admin_bp.cli.command("create_admin_user")
def create_admin():
    """Create an admin account."""
    retries = 3

    name = input("Please enter the admin full name: ")
    username = input("Please enter the admin username: ")
    number = input("Please enter the admin contact number: ")
    address = input("Please enter the admin address: ")
    status = "active"
    type = "admin"
    password = getpass("Please enter the admin password: ")

    while retries != 0:
        if UserModel.find_by_username(username):
            print("The username already exists.")
            break

        confirm = getpass("Please re-enter the admin password: ")
        if safe_str_cmp(password, confirm):
            user = UserModel(username, name, password, number, address, status, type)
            user.save_to_db()

            print(f"Welcome {name}.")

            break

        print("Password does not match.")
        retries -= 1
    else:
        print("You have exceeded the maximum retry. Please try again.")
