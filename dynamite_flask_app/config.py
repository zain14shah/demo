"""This file contains all the configurations for the application."""

DEBUG = True
PORT = 4000
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
SQLALCHEMY_TRACK_MODIFICATIONS = False
