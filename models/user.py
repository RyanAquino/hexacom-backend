from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))

    job_orders = db.relationship("JobOrderModel", lazy="dynamic")

    def __init__(self, username, name, password):
        self.username = username
        self.name = name
        self.password = password

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
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
