from flask import Blueprint

# from models.brands import BrandModel
from models.user import UserModel
from models.joborders import JobOrderModel
import click

seeder_bp = Blueprint("seeder", __name__)
brands = ["Asus", "Lenovo", "HP", "Dell", "Apple"]
users = [
    ["bob", "Bob Durie", "bob", "098712374918", "bob's address", "active", "user"],
    ["jo", "Jo Michigan", "jo", "098731232134", "jo's address", "active", "user"],
    ["john", "John Dough", "john", "09321314114", "john's address", "active", "user"],
    ["vo", "Vo Vooughan", "vo", "09321231231", "vo's address", "active", "user"],
    ["jean", "Jean Burton", "jean", "09321231231", "jean's address", "active", "user"],
]
job_orders = [
    ["JO0000001", "Laptop", "Fix battery"],
    ["JO0000002", "Laptop", "Fix Screen"],
    ["JO0000003", "Laptop", "Fix keyboard"],
    ["JO0000004", "Laptop", "Fix mouse pad"],
    ["JO0000005", "Laptop", "Fix power"],
]


@seeder_bp.cli.command("all")
@click.option("--remove/--add", default=False)
def seed(remove):
    for i in range(len(brands)):
        # brand = BrandModel.find_by_name(brands[i])
        job_order = JobOrderModel.find_by_id(job_orders[i][0])
        user = UserModel.find_by_username(users[i][0])

        if remove:
            print(f"Removing sample dataset {i+1}..")
            if job_order:
                job_order.delete_from_db()
            # if brand:
            #     brand.delete_from_db()
            if user:
                user.delete_from_db()
        else:
            print(f"Creating dataset {i+1}..")
            # brand = BrandModel(brands[i])
            # brand.save_to_db()

            user = UserModel(*users[i])
            user.save_to_db()

            job_order = JobOrderModel(*job_orders[i], brands[i], user.id)
            job_order.save_to_db()


@seeder_bp.cli.command("users")
@click.option("--remove/--add", default=False)
def user_seeder(remove):
    print("User Seeder")
    for i in range(len(users)):
        user = UserModel.find_by_username(users[i][0])
        if remove:
            if user:
                print(f"Removing user {i+1}..")
                user.delete_from_db()
            else:
                print(f"User {i+1} does not exist.")
        else:
            if not user:
                print(f"Creating user {i+1}..")
                user = UserModel(*users[i])
                user.save_to_db()
            else:
                print(f"User {i+1} already exists.")


# @seeder_bp.cli.command("brands")
# @click.option("--remove/--add", default=False)
# def brand_seeder(*remove):
#     print("Brand Seeder")
#     for i in range(len(brands)):
#         brand = BrandModel.find_by_name(brands[i])
#         if remove:
#             if brand:
#                 print(f"Removing brand {i+1}..")
#                 brand.delete_from_db()
#             else:
#                 print(f"Brand {i+1} does not exist.")
#         else:
#             if not brand:
#                 print(f"Creating brand {i+1}..")
#                 brand = BrandModel(brands[i])
#                 brand.save_to_db()
#             else:
#                 print(f"Brand {i+1} already exists.")
#
@seeder_bp.cli.command("job_orders")
@click.option("--remove/--add", default=False)
def job_order_seeder(remove):
    print("Job Order Seeders")
    for i in range(len(job_orders)):
        job_order = JobOrderModel.find_by_id(job_orders[i][0])
        if remove:
            if job_order:
                print(f"Removing job orders {i+1}..")
                job_order.delete_from_db()
            else:
                print(f"Job Order {i+1} not found.")
        else:
            user = UserModel.find_by_username(users[i][0])

            if user:
                print(f"Creating job orders {i+1}..")
                job_order = JobOrderModel(*job_orders[i], brands[i], user.id)
                job_order.save_to_db()
            else:
                print(
                    "Please create brands and users first by using flask seeder <users or brands or all>"
                )
