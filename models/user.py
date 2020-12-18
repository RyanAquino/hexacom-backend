from db import db
import enum


class Status(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Types(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    number = db.Column(db.String(20))
    address = db.Column(db.String(100))
    status = db.Column(db.Enum(Status))
    type = db.Column(db.Enum(Types))

    job_orders = db.relationship("JobOrderModel", lazy="dynamic")

    def __init__(self, username, name, password, number, address, status, type):
        self.username = username
        self.name = name
        self.password = password
        self.number = number
        self.address = address
        self.status = status
        self.type = type

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "number": self.number,
            "address": self.address,
            "status": self.status.value,
            "type": self.type.value,
            "job_orders": [job_order.json() for job_order in self.job_orders.all()],
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def switch(self):
        stat = "activated"

        if self.status.value == "active":
            self.status = "inactive"
            stat = "deactivated"
        else:
            self.status = "active"

        db.session.commit()
        return stat

    def change_password(self, new_password):
        self.password = new_password
        db.session.commit()
