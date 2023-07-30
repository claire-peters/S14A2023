from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('postgres_connection_string')
# initialize the app with the extension
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String)
    email = db.Column(db.String)
    phonenumber = db.Column(db.String)
    status = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean)
    orders = db.relationship('Order', backref='user')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_name = db.Column(db.String)
    item_count = db.Column(db.Integer)
    total = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
