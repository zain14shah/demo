"""
This module gives us endpoints to access our APIs.
"""

from init import api, app
from resources.product import Products, ProductById
from resources.user import User, Session


api.add_resource(Products, '/products')
api.add_resource(ProductById, '/product/<int:product_id>')
api.add_resource(User, '/user')
api.add_resource(Session, '/session')


if __name__ == '__main__':
    app.run()
