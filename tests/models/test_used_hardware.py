from models.used_hardware import UsedHardwareModel
from db import db


def test_find_by_hardware_id(app):
    with app.app_context():
        hardware = UsedHardwareModel(hardware_id=1, employee_id=1)
        db.session.add(hardware)
        db.session.commit()

        hardware_db = UsedHardwareModel.find_by_hardware_id(hardware.id)
        assert hardware_db.hardware_id == hardware.hardware_id
        assert hardware_db.employee_id == hardware.employee_id
        assert hardware_db.id == hardware.id


def test_find_by_employee_id(app):
    with app.app_context():
        hardware = UsedHardwareModel(hardware_id=1, employee_id=1)
        db.session.add(hardware)
        db.session.commit()

        hardware_db = UsedHardwareModel.find_by_employee_id(hardware.id)
        assert isinstance(hardware_db, list)
        assert len(hardware_db) == 1
        assert hardware_db[0].hardware_id == hardware.hardware_id
        assert hardware_db[0].employee_id == hardware.employee_id


def test_get_all(app):
    with app.app_context():
        hardware = UsedHardwareModel(hardware_id=1, employee_id=1)
        db.session.add(hardware)
        db.session.commit()

        hardware_db = UsedHardwareModel.get_all()
        assert isinstance(hardware_db, list)
        assert len(hardware_db) == 1


def test_save_link(app):
    with app.app_context():
        hardware = UsedHardwareModel(hardware_id=1, employee_id=1)
        hardware.save_link()

        hardware_db = UsedHardwareModel.find_by_hardware_id(hardware.id)
        assert hardware_db is not None


def test_delete_link(app):
    with app.app_context():
        hardware = UsedHardwareModel(hardware_id=1, employee_id=1)
        db.session.add(hardware)
        db.session.commit()
        hardware.delete_link()

        hardware_db = UsedHardwareModel.find_by_hardware_id(hardware.id)
        assert hardware_db is None


def test_delete_links(app):
    with app.app_context():
        hardware_1 = UsedHardwareModel(hardware_id=1, employee_id=1)
        db.session.add(hardware_1)
        db.session.commit()

        hardware_2 = UsedHardwareModel(hardware_id=2, employee_id=1)
        db.session.add(hardware_2)
        db.session.commit()

        hardware_count = UsedHardwareModel.delete_links(hardware_1.employee_id)

        hardware_db_1 = UsedHardwareModel.find_by_hardware_id(hardware_1.id)
        hardware_db_2 = UsedHardwareModel.find_by_hardware_id(hardware_2.id)
        assert hardware_db_1 is None
        assert hardware_db_2 is None
        assert hardware_count == 2
