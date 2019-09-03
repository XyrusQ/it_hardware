from db import db


class HardwareModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_hardware(self):
        db.session.add(self)
        db.session.commit()

    def delete_hardware(self):
        db.session.delete(self)
        db.session.commit()
