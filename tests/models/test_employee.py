from models.employee import EmployeeModel
from db import db


def test_find_by_id(app):
    with app.app_context():
        employee = EmployeeModel(first_name='test', second_name='test2', username='test3')
        db.session.add(employee)
        db.session.commit()

        employee_db = EmployeeModel.find_by_id(employee.id)
        assert employee_db.first_name == employee.first_name
        assert employee_db.second_name == employee.second_name
        assert employee_db.username == employee.username
        assert employee_db.id == employee.id


def test_find_by_username(app):
    with app.app_context():
        employee = EmployeeModel(first_name='test', second_name='test2', username='test3')
        db.session.add(employee)
        db.session.commit()

        employee_db = EmployeeModel.find_by_username(employee.username)
        assert employee_db.first_name == employee.first_name
        assert employee_db.second_name == employee.second_name
        assert employee_db.username == employee.username
        assert employee_db.id == employee.id


def test_get_all(app):
    with app.app_context():
        employee = EmployeeModel(first_name='test', second_name='test2', username='test3')
        db.session.add(employee)
        db.session.commit()

        employee_db = EmployeeModel.get_all()
        assert isinstance(employee_db, list)
        assert len(employee_db) == 1


def test_save_employee(app):
    with app.app_context():
        employee = EmployeeModel(first_name='test', second_name='test2', username='test3')
        employee.save_employee()

        employee_db = EmployeeModel.find_by_id(employee.id)
        assert employee_db is not None


def test_delete_employee(app):
    with app.app_context():
        employee = EmployeeModel(first_name='test', second_name='test2', username='test3')
        db.session.add(employee)
        db.session.commit()
        employee.delete_employee()

        employee_db = EmployeeModel.find_by_id(employee.id)
        assert employee_db is None
