from app import app
from db import db

db.init_app(app)


@app.before_first_request
def before_first_request_func():
    db.create_all()
