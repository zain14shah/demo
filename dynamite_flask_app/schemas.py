"""This module creates the schemas required to parse database tables to resources."""

from models import Product, Size, User
from init_db import ma


class ProductSchema(ma.ModelSchema):

    class Meta:
        model = Product

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
