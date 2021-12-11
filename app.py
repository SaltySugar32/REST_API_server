""" File with app configs and db """
import os
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import config


app = Flask(__name__)
database = SQLAlchemy(app)
jwtManager = JWTManager(app)

if os.environ["FLASK_ENV"] == "prod":
    app.config.from_object(config.ProdConfig)
else:
    app.config.from_object(config.DevConfig)


class User(database.Model, UserMixin):
    """ User Model """
    __tablename__ = "users"
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), nullable=False, unique=True)
    password = database.Column(database.String(20), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password = generate_password_hash(kwargs['password'])

    def __repr__(self):
        return f'<User id: {self.id}, username: {self.username}, password: {self.password}>'

    @classmethod
    def auth(cls, username, password):
        """ authorize user """
        user = cls.query.filter(cls.username == username).first()
        if user is None:
            return 0
        if not check_password_hash(user.password, password):
            return 1
        return user

    def get_token(self, expire_time=24):
        """ get user token """
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.username, expires_delta=expire_delta)
        return token

    def save_in_database(self):
        """ save changes in database """
        database.session.add(self)
        database.session.commit()
        return 'New user registered: ' + self.username


class Todo(database.Model):
    """ Task Model """
    __tablename__ = "todos"
    id = database.Column(database.Integer, primary_key=True)
    description = database.Column(database.Text)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    user = database.relationship("User", backref="tasks")

    def __init__(self, *args, **kwargs):
        super(Todo, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<TODO id: {}, description: {}, user id: {}>'.format(self.id, self.description, self.user_id)

    def save_in_database(self):
        """ save changes in database """
        database.session.add(self)
        database.session.commit()
        return self.id

    def delete_from_database(self):
        """ save changes in database """
        database.session.delete(self)
        database.session.commit()
        return 1
