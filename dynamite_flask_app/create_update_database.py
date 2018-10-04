"""This module creates and updates the database tables."""

import json
import random

from init_db import db
from models import User, Product, Order, ImageUrl, Feature, ProductSize, Size, Category, Feature, ActiveToken
from resources.user import add_new_user


with open('products.json') as file:
    """Load the products.json file into the products variable."""
    products = json.load(file)

users = [
    {
        'name': 'Zain',
        'email': 'abc@123.com',
        'password': 'asd123',
        'address': 'abc',
        'contact_no': 123,
    },
    {
        'name': 'Ali',
        'email': 'abc1@123.com',
        'password': 'asd123',
        'address': 'ab2c',
        'contact_no': 1523,
    },
    {
        'name': 'Shah',
        'email': 'abcfff1@123.com',
        'password': 'asd123',
        'address': 'ab2cs',
        'contact_no': 12345523,
    },
    {
        'name': 'Ahmed',
        'email': 'abhhewc1@123.com',
        'password': 'asd123',
        'address': 'ab2erc',
        'contact_no': 176474523,
    },
    {
        'name': 'Boy',
        'email': 'furrfurr@123.com',
        'password': 'asd123',
        'address': 'fwefeew',
        'contact_no': 8484876,
    }
]

orders = [
    {
        'date': '2008, 4, 12'
    },
    {
        'date': '2018, 12, 02'
    }
]


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
        Product(str): Each product, used from the add_products() method.
        product_details: Add product to the database, also used to create relationship with the Product table.

    """
    for image_url in product['img_urls']:
        url = ImageUrl(url=image_url)
        product_details.img_urls.append(url)


def add_feature(product, product_details):
    """adds features to the database.

    Args:
        Product(str): Each product, used from the add_products() method.
        product_details: Add product to the database, also used to create relationship with the Product table.

    """
    for detail in product['details']:
        feature = Feature.query.filter_by(feature=detail).first()
        if feature is None:
            feature = Feature(feature=detail)
        product_details.features.append(feature)


def add_size(product, product_details):
    """adds sizes to the database.

    Args:
        Product(str): Each product, used from the add_products() method.
        product_details: Add product to the database, also used to create relationship with the Product table.

    """
    for each_size in product['sizes']:
        each_size = each_size.upper()
        available = ProductSize(availability=bool(random.getrandbits(1)))

        size = Size.query.filter_by(size=each_size).first()

        if size is None:
            size = Size(size=each_size)

        available.size = size
        available.product = product_details


def add_category(product_details):
    """adds categories to the database.

    Args:
        product_details: Add product to the database, also used to create relationship with the Product table.

    """
    category = Category.query.filter_by(type='General').first()
    if category is None:
        category = Category()
    product_details.categories.append(category)


def add_user():
    """adds users to the database."""
    for user in users:
        add_new_user(user['name'], user['email'],
                     user['password'], user['address'], user['contact_no'])

    db.session.commit()


def add_order(user, product):
    """adds orders to the database.

    Args:
        user(int): The user ID.
        product(int): The product ID

    """
    user_id = User.query.get(user)
    product_id = Product.query.get(product)
    order_details = Order()
    user_id.orders.append(order_details)
    product_id.orders.append(order_details)

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
