from db import db


class EmployeeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_employee(self):
        db.session.add(self)
        db.session.commit()

    def delete_employee(self):
        db.session.delete(self)
        db.session.commit()
