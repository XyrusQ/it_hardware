import pytest
from flask import testing

from app import app as main_app
from db import db


class TestClient(testing.FlaskClient):
    def open(self, *args, **kwargs):
        api_key_header = {'X-API-KEY': 'CHANGE_ME'}

        headers = kwargs.pop('headers', {})
        if headers.get('X-API-KEY', None) is None:
            headers.update(api_key_header)

        kwargs['headers'] = headers
        return super().open(*args, **kwargs)


@pytest.fixture
def app():

    main_app.config['TESTING'] = True
    main_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'

    with main_app.app_context():
        db.init_app(main_app)
        db.create_all()

    yield main_app

    with main_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    app.test_client_class = TestClient
    return app.test_client()
