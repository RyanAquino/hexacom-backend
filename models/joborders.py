from db import db
from datetime import datetime


class JobOrderModel(db.Model):
    __tablename__ = "joborders"

    id = db.Column(db.String(80), primary_key=True)
    item = db.Column(db.String(80))
    job_description = db.Column(db.String(80))
    date_received = db.Column(db.DateTime, server_default=db.func.now())
    date_released = db.Column(db.DateTime)

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    user = db.relationship("UserModel", backref="users")

    # brand_id = db.Column(
    #     db.Integer, db.ForeignKey("brands.id", ondelete="RESTRICT"), nullable=False
    # )
    # brand = db.relationship("BrandModel", backref="brands")

    brand_id = db.Column(db.String(80), nullable=False)

    def __init__(self, _id, item, job_description, brand_name, technician_id):
        self.id = _id
        self.item = item
        self.job_description = job_description
        self.user_id = technician_id
        self.brand_id = brand_name

    def json(self):
        return {
            "job_id": self.id,
            "item": self.item,
            "job_description": self.job_description,
            "date_received": self.date_received.strftime("%b %d, %Y %I:%M"),
            "date_released": self.date_released.strftime("%b %d, %Y %I:%M")
            if self.date_released
            else None,
            "brand": self.brand_id,
            "technician_name": self.user.username,
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def update_release_date(self):
        self.date_released = datetime.now()
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
