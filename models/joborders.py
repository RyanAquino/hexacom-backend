from db import db


class JobOrderModel(db.Model):
    __tablename__ = "joborders"

    id = db.Column(db.String(80), primary_key=True)
    technician_name = db.Column(db.String(80))
    item = db.Column(db.String(80))
    job_description = db.Column(db.String(80))

    def __init__(self, id, technician_name, item, job_description):
        self.id = id
        self.technician_name = technician_name
        self.item = item
        self.job_description = job_description

    def json(self):
        return {
            "job_id": self.id,
            "technician_name": self.technician_name,
            "item": self.item,
            "job_description": self.job_description,
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
