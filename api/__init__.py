import os

from flask_restplus import Api
from flask import request

from .employees import api as employees_api
from .hardware import api as hardware_api

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}


def auth_required(func):
    def check_auth(*args, **kwargs):
        if 'X-API-KEY' not in request.headers and request.path != '/swagger.json':
            return {'message': 'API key required'}, 401

        key = request.headers.get('X-API-KEY')
        if key != os.getenv('X_API_KEY', 'CHANGE_ME') and request.path != '/swagger.json':
            return {'message': 'Incorrect API key'}, 401

        return func(*args, **kwargs)
    check_auth.__name__ = func.__name__
    check_auth.__doc__ = func.__doc__
    return check_auth


api = Api(version='1.0', title='IT Hardware API', description='A simple API to manage IT hardware',
          authorizations=authorizations, security='apikey', decorators=[auth_required])

api.add_namespace(employees_api)
api.add_namespace(hardware_api)
