from models.hardware import HardwareModel
from db import db


def test_find_by_id(app):
    with app.app_context():
        hardware = HardwareModel(name='test', category='laptop')
        db.session.add(hardware)
        db.session.commit()

        hardware_db = HardwareModel.find_by_id(hardware.id)
        assert hardware_db.name == hardware.name
        assert hardware_db.category == hardware.category
        assert hardware_db.id == hardware.id


def test_get_all(app):
    with app.app_context():
        hardware = HardwareModel(name='test', category='laptop')
        db.session.add(hardware)
        db.session.commit()

        hardware_db = HardwareModel.get_all()
        assert isinstance(hardware_db, list)
        assert len(hardware_db) == 1


def test_save_hardware(app):
    with app.app_context():
        hardware = HardwareModel(name='test', category='laptop')
        hardware.save_hardware()

        hardware_db = HardwareModel.find_by_id(hardware.id)
        assert hardware_db is not None


def test_delete_hardware(app):
    with app.app_context():
        hardware = HardwareModel(name='test', category='laptop')
        db.session.add(hardware)
        db.session.commit()
        hardware.delete_hardware()

        hardware_db = HardwareModel.find_by_id(hardware.id)
        assert hardware_db is None
