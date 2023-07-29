from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the database
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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


with app.app_context():
    db.create_all()

    # Query the whole table
    users = db.session.execute(
        db.select(User).order_by(User.username)).scalars()
    for u in users:
        print(u.as_dict())
    print("==========After Select All 1===============")

    # Insert a new object
    user1 = User(
        username="username1",
        email="email1@example.com",
    )
    db.session.add(user1)
    db.session.commit()
    print("==========After Commit===============")
    # Query the whole table
    userList = db.session.execute(
        db.select(User).order_by(User.username)).scalars()
    for s in userList:
        print(s.as_dict())
    print("==========After Select All 2===============")
    # Query by id, a specific record
    user = db.get_or_404(User, 1)
    print(user.as_dict())
