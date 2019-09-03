import os

from flask import Flask
from flask_restplus import Api

from db import db
from api import api

app = Flask(__name__)
api.init_app(app)

app.config['BUNDLE_ERRORS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE', 'sqlite:///example.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'CHANGE_ME'
