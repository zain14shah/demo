"""This module creates the User resources used for all the security features of the application,
which includes signing in, signing up and signing out.

"""

from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jti,
                                get_jwt_identity, jwt_refresh_token_required, get_raw_jwt, jwt_required)
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash


from init import db, jwt
from models import User, ActiveToken


def generate_token(email):
    """Creates access and refresh tokens for users based on their email addresses whih are unique.

    Args:
        email(str): To be used as an identity to create JWTs.

    Returns:
        access_token(str) and refresh_token(str)
    """
    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)
    active_refresh_token = ActiveToken(access_jti=get_jti(
        access_token), refresh_jti=get_jti(refresh_token))
    db.session.add(active_refresh_token)
    db.session.commit()

    return access_token, refresh_token


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """This loader extends the functionality of jwt decorators and checks if the 
    dycrypted token exists in the ActiveToken table or not.

    Args:
        decrypted_token(str): access_token if a function with @jwt_required decoratore is accessed,
                              refresh_token if a function with @jwt_refresh_token_required decorator is accessed.

    Returns:
        bool: True if successful, False otherwise.
        We take the opposite of the bool value, as the loader is to check blacklisted tokens, where as we are using the
        opposite of this functionality.

    """
    jti = decrypted_token['jti']
    if decrypted_token['type'] == 'refresh':
        is_active_login = ActiveToken.query.filter_by(refresh_jti=jti).first()
    elif decrypted_token['type'] == 'access':
        is_active_login = ActiveToken.query.filter_by(access_jti=jti).first()

    return not bool(is_active_login)


def add_new_user(name, email, password, address, contact_no):
    """Adds a new user to the database. These details will be collected form the user upon sign up.

    Args:
        name(str): User's name.
        email(str): User's email, this they will use when they login.
        password(str): This will be encrypted before being saved in the database, also needed upon login.
        address(str): User's address.
        contact_no(int): User's contact number.
    """

    new_user = User(
        name=name, email=email, password=generate_password_hash(password, method='sha256'), address=address,
        contact_no=contact_no
    )

    db.session.add(new_user)


class NewUser(Resource):
    """Resource for creating a user, also called signup."""

    def post(self):
        """This method creates a new user and authenticates the user session, also called register/signup.

        Args:
            name(str) = Name of the user.
            email(str): A unique user email address, which does not already exist in the database.
            password(str): A password for authentication, this is encrypted before being saved in the database.
            address(str) = User's address.
            contact_no(int) = User's contact number.

        Returns:
            message(str): Error, if email already exists.
            message(str): Notifying the user that he/she has signed up successfully,
            access_token(str): Used to access all methods that require JWT authentication,
            refresh_token(str): Used to create a new access_token, when it expires, if all credentials are accepted.

        """
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        address = request.form.get('address')
        contact_no = request.form.get('contact_no')

        user = User.query.filter_by(email=email).first()
        if user:
            return {'Error': 'Email already exists'}

        add_new_user(name, email, password, address, contact_no)

        access_token, refresh_token = generate_token(email)

        return {
            'message': f'Hi {name}, you have signed up successfully.',
            'access_token': access_token,
            'refresh_token': refresh_token
        }


class Session(Resource):
    """This resource deals with all the sessioon functionality."""

    def post(self):
        """This method authenticates the user session, also called login/signin.

        Args:
            email(str): A unique, already registered, user email address.
            password(str): A password for authentication, this is matched againt the password in the database.

        Returns:
            message(str): Error, if email does not exist in the database.
            message(str): Error, if password does not match.
            message(str): Notifying the user that he/she has logged in successfully,
            access_token(str): Used to access all methods that require JWT authentication,
            refresh_token(str): Used to create a new access_token, when it expires, if all credentials are accepted.

        """
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            return {'Error': f'The email address \'{email}\' does not exist'}

        correct_password = check_password_hash(user.password, password)

        if not correct_password:
            return {'Error': 'You have entered an incorrect password'}

        access_token, refresh_token = generate_token(email)

        return {
            'message': f'Logged in as {user.name}',
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    @jwt_refresh_token_required
    def put(self):
        """Used to update the user session, after the access token has expired.

        Args:
            refresh_token(str): Provided upon login/signup.

        Returns:
            access_token(str): Used to access all protected methods, that require JWT authentication.

        """
        jti = get_raw_jwt()['jti']
        refresh_access_pair = ActiveToken.query.filter_by(
            refresh_jti=jti).first()

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        refresh_access_pair.access_jti = get_jti(access_token)
        db.session.commit()
        return {'access_token': access_token}

    @jwt_required
    def delete(self):
        """This is the logout method. It deletes both, access and refresh, tokens from the database so that they can
        no longer be used.

        Args:
            access_token(str): Provided upon login/signup.

        Returns:
            message(str): Notifies the user that he'she has been logged out.

        """
        jti = get_raw_jwt()['jti']
        access_refresh_pair = ActiveToken.query.filter_by(
            access_jti=jti).first()
        db.session.delete(access_refresh_pair)
        db.session.commit()
        return {'message': 'You have successfully logged out.'}
