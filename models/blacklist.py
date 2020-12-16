from db import db


class Blacklist(db.Model):
    __tablename__ = "blacklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.Text)

    def __init__(self, jti):
        self.jti = jti

    @classmethod
    def verify_token(cls, jti):
        print(jti)
        return True if cls.query.filter_by(jti=jti).first() else False

    def add(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "access_token": self.jti,
        }
