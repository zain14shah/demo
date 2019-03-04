"""This module creates the schemas required to parse database tables to resources."""

from models import Product
from init import marshal


class ProductSchema(marshal.ModelSchema):

    class Meta:
        model = Product
