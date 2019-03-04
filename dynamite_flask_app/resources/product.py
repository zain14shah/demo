"""Product resource REST API module."""

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models import Product, Size
from schemas import ProductSchema


class Products(Resource):
    """Creates Product resource that uses the Porduct model for required results."""

    def get(self):
        """May take multiple arguments provided in the API. Also has pagination functionality.
        Will also work without any arguments.

        Args:
            size(str, optional): The porduct size that needs to be searched.
            page(int, optional): The page number of the results.

        Returns:
            Details of all products of the required size or all product details if no arguments, or only page
            number, provided.
        """
        required_size = request.args.get('size', '').upper()
        page = request.args.get('page', 1)

        query = Product.query

        if required_size:
            size = Size.query.filter_by(size=required_size).first()
            if not size:
                return {'Error': 'You have enterend an invalid size.'}

            query = query.filter(Product.sizes.any(
                size=size, availability=True))

        products = query.paginate(page=int(page), per_page=10)

        products_schema = ProductSchema(many=True)

        return products_schema.jsonify(products.items)


class ProductById(Resource):
    """Get product by given ID."""
    @jwt_required
    def get(self, product_id):
        """Can only be accessed by an authenticated user. Provides the details for the given product's ID.

        Args:
            product_id(int): ID of the required product.

        Returns:
            Details of the required product.
        """
        product = Product.query.get(product_id)

        if not product:
            return {'Error': 'This product does not exist'}

        product_schema = ProductSchema()

        return product_schema.jsonify(product)
