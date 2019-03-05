from flask import request, jsonify, redirect, url_for, flash
from werkzeug.security import generate_password_hash

from init import app, db, login_manager
from models import Product, Size, User
from schemas import product_schema, products_schema


def get_product_for_id(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'Error': 'This product does not exist'})
    return product_schema.jsonify(product)


def get_product_for_size(required_size, page=1):
    size = Size.query.filter_by(size=required_size).first()

    if not size:
        return jsonify({'Error': 'You have enterend an invalid size.'})

    products = Product.query.filter(Product.sizes.any(
        size=size, availability=True
    )).paginate(page=int(page), per_page=10)

    # if not products.has_next:

    return products_schema.jsonify(products.items)


def get_all_products(page=1):
    all_products = Product.query.paginate(page=int(page), per_page=10).items
    result = products_schema.dump(all_products)
    return jsonify(result.data)

def signup_post(name, email, password, address, contact_no):
    user = User.query.filter_by(email=email).first()
    if user:
        return ('Email already exists')
        # flash('Email already exists')
        # return redirect(url_for('signup'))

    new_user = User(
        name=name, email=email, password=generate_password_hash(password, method='sha256'), address=address,
        contact_no=contact_no
    )

    db.session.add(new_user)
    db.session.commit()

    return ('Hi ' + name + ' You have signed up successfully.')

@app.route('/')
def index():
    return ('<h1>Hello!!\nWelcome to my app.</h1>')

@login_manager.user_loader
def load_user(user_id):
    user_id = User.query.get(user_id)
    return user_id

@app.route('/signup', methods=['GET'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    address = request.form.get('address')
    contact_no = request.form.get('contact_no')

    return signup_post(name, email, password, address, contact_no)


# @app.route('/login', methods=['GET', 'POST'])
# def login():


@app.route('/products', methods=['GET'])
def get_product():
    product_id = request.args.get('id')
    required_size = request.args.get('size', '').upper()
    page = request.args.get('page', 1)

    if product_id:
        return get_product_for_id(product_id)
    elif required_size:
        return get_product_for_size(required_size, page)
    else:
        return get_all_products(page)


# if __name__ == '__main__':
    # app.run(debug=True)
