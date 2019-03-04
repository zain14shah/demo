"""This module creates all the neccessary objects that will be used in the application."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.py')
app.config.from_pyfile('secrets.py')
api = Api(app)
db = SQLAlchemy(app)
marshal = Marshmallow(app)
jwt = JWTManager(app)
