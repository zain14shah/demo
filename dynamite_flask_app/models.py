"""This module contains all the models and the relationship tables for each of them."""

import datetime

from init import db


product_order = db.Table('product_order',
         db.Column('product_id', db.Integer, db.ForeignKey(
             'product._id'), primary_key=True),
         db.Column('order_id', db.Integer, db.ForeignKey(
             'order._id'), primary_key=True)
         )

product_feature = db.Table('product_feature',
         db.Column('product_id', db.Integer, db.ForeignKey(
             'product._id'), primary_key=True),
         db.Column('feature_id', db.Integer, db.ForeignKey(
             'feature._id'), primary_key=True)
         )

product_category = db.Table('product_category',
         db.Column('product_id', db.Integer, db.ForeignKey(
             'product._id'), primary_key=True),
         db.Column('category_id', db.Integer, db.ForeignKey(
             'category._id'), primary_key=True)
         )


class ProductSize(db.Model):
    """The association object for the product and size tables."""
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product._id'), primary_key=True)
    size_id = db.Column(db.Integer, db.ForeignKey(
        'size._id'), primary_key=True)
    availability = db.Column(db.Boolean, nullable=False)

    product = db.relationship('Product', back_populates='sizes')
    size = db.relationship('Size', back_populates='products')


class Product(db.Model):
    """The product table."""
    _id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    sale_price = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    sizes = db.relationship('ProductSize', back_populates='product')
    img_urls = db.relationship('ImageUrl', backref='product', lazy=True)


class User(db.Model):
    """The user table."""
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    contact_no = db.Column(db.Integer, nullable=False)

    orders = db.relationship('Order', backref='user', lazy=True)


class Order(db.Model):
    """The order table."""
    _id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)

    products = db.relationship(
        'Product', secondary=product_order, backref=db.backref('orders', lazy=True))


class Category(db.Model):
    """The Category table."""
    _id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False, default='General')

    products = db.relationship(
        'Product', secondary=product_category, backref=db.backref('categories', lazy=True))


class Size(db.Model):
    """The Size table."""
    _id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String, nullable=False)

    products = db.relationship('ProductSize', back_populates='size')


class Feature(db.Model):
    """The feature table."""
    _id = db.Column(db.Integer, primary_key=True)
    feature = db.Column(db.String, nullable=False)

    products = db.relationship(
        'Product', secondary=product_feature, backref=db.backref('features', lazy=True))


class ImageUrl(db.Model):
    """The image_url table."""
    _id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product._id'), nullable=False)


class ActiveToken(db.Model):
    """The active_token table."""
    _id = db.Column(db.Integer, primary_key=True)
    access_jti = db.Column(db.String)
    refresh_jti = db.Column(db.String)
