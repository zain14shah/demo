"""This file contains all the configurations for the application."""

DEBUG = True
PORT = 4000
SQLALCHEMY_DATABASE_URI = 'postgresql://zainshah:123123@localhost/dynamite_db'
JWT_SECRET_KEY = 'secretkey'
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
SQLALCHEMY_TRACK_MODIFICATIONS = False
