from db import db


class UsedHardwareModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hardware_id = db.Column(db.Integer, db.ForeignKey('hardware_model.id'))
    hardware = db.relationship('HardwareModel')
    employee_id = db.Column(db.Integer, db.ForeignKey('employee_model.id'))
    employee = db.relationship('EmployeeModel')

    @classmethod
    def find_by_hardware_id(cls, id):
        return cls.query.filter_by(hardware_id=id).first()

    @classmethod
    def find_by_employee_id(cls, employee_id):
        return cls.query.filter_by(employee_id=employee_id).all()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_link(self):
        db.session.add(self)
        db.session.commit()

    def delete_link(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def delete_links(cls, employee_id):
        links_count = cls.query.filter_by(employee_id=employee_id).delete()
        db.session.commit()
        return links_count
