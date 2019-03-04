"""This module creates and updates the database tables."""

import json
import random

from init import db
from models import User, Product, Order, ImageUrl, Feature, ProductSize, Size, Category, Feature, ActiveToken
from resources.user import add_new_user


with open('products.json') as file:
    """Load the products.json file into the products variable."""
    products = json.load(file)


def add_products():
    """Adds all products with their details to the database."""
    for product in products:
        product_details = Product(
            product_id=product['id'], name=product['name'], price=product['price'], sale_price=product['sale_price'],
            description=product['description']
        )

        add_image_url(product, product_details)
        add_feature(product, product_details)
        add_category(product_details)
        add_size(product, product_details)

        db.session.add(product_details)

    db.session.commit()


def add_image_url(product, product_details):
    """Adds image urls to the database.

    Args:
        product(obj): parsed json of a product.
        product_details: product object from the database.

    """
    for image_url in product['img_urls']:
        url = ImageUrl(url=image_url)
        product_details.img_urls.append(url)


def add_feature(product, product_details):
    """Args:
        product(obj): parsed json of a product.
        product_details: product object from the database.

    """
    for detail in product['details']:
        feature = Feature.query.filter_by(feature=detail).first()
        if feature is None:
            feature = Feature(feature=detail)
        product_details.features.append(feature)


def add_size(product, product_details):
    """adds sizes to the database.

    Args:
        product(obj): parsed json of a product.
        product_details: product object from the database.

    """
    for each_size in product['sizes']:
        each_size = each_size.upper()
        set_availability = ProductSize(availability=bool(random.getrandbits(1)))

        size = Size.query.filter_by(size=each_size).first()

        if size is None:
            size = Size(size=each_size)

        set_availability.size = size
        set_availability.product = product_details


def add_category(product_details):
    """adds categories to the database.

    Args:
        product_details: product object from the database.

    """
    category = Category.query.filter_by(type='General').first()
    if category is None:
        category = Category()
    product_details.categories.append(category)


def add_user():
    """creates user table in the database."""


def add_order(user_id, product_id):
    """adds orders to the database.

    Args:
        user_id(int): The user ID.
        product_id(int): The product ID

    """
    user = User.query.get(user_id)
    product = Product.query.get(product_id)
    order_details = Order()
    user.orders.append(order_details)
    product.orders.append(order_details)

    db.session.add(order_details)
    db.session.commit()


def setup_database():
    """Sets up the database tables and adds data to it by using methods given below. Also creates orders and populates
    the order table if any.
    """
    db.drop_all()
    db.create_all()
    add_products()
    add_user()
    option = input('Want to place an order? Enter Y to continue: ')
    while option.capitalize() == 'Y':
        user = input('Enter User ID: ')
        product = input('Enter Product ID: ')
        add_order(user, product)
        print('Order added!!')
        option = input('Enter Y to add another: ')


if __name__ == '__main__':
    setup_database()
