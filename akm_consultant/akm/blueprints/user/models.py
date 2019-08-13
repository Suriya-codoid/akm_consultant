from datetime import datetime
from collections import OrderedDict
from hashlib import md5

import pytz
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from itsdangerous import URLSafeTimedSerializer, \
    TimedJSONWebSignatureSerializer

from lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from ...extensions import db, Serializer


# class User(UserMixin, ResourceMixin, db.Model):
class User(UserMixin, db.Model, Serializer):
    ROLE = OrderedDict([
        ('member', 'Member'),
        ('admin', 'Admin'),
        ('superadmin', 'SuperAdmin'),
        ('tech support', 'TechSupport')
    ])

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # Authentication.
    role = db.Column(db.Enum(*ROLE, name='role_types', native_enum=False), index=True, nullable=False,
                     server_default='member')
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       server_default='1')
    email = db.Column(db.String(255), unique=True, index=True, nullable=False,
                      server_default='')
    full_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(128), nullable=False, server_default='')

    # Activity tracking.
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(db.DateTime(), default=datetime.utcnow)
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_on = db.Column(db.DateTime(), default=datetime.utcnow)
    last_sign_in_ip = db.Column(db.String(45))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(User, self).__init__(**kwargs)

        self.password = User.encrypt_password(kwargs.get('password', ''))

    @classmethod
    def find_by_identity(cls, email):
        """
        Find a user by their e-mail or username.

        :param identity: Email or username
        :type identity: str
        :return: User instance
        """
        return User.query.filter(User.email == email).first()

    @classmethod
    def encrypt_password(cls, plaintext_password):
        """
        Hash a plaintext string using PBKDF2. This is good enough according
        to the NIST (National Institute of Standards and Technology).

        In other words while bcrypt might be superior in practice, if you use
        PBKDF2 properly (which we are), then your passwords are safe.

        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str
        """
        if plaintext_password:
            return generate_password_hash(plaintext_password)

        return None

    @classmethod
    def deserialize_token(cls, token):
        """
        Obtain a user from de-serializing a signed token.

        :param token: Signed token.
        :type token: str
        :return: User instance or None
        """
        private_key = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'])
        try:
            decoded_payload = private_key.loads(token)

            return User.find_by_identity(decoded_payload.get('user_email'))
        except Exception:
            return None

    def is_active(self):
        """
        Return whether or not the user account is active, this satisfies
        Flask-Login by overwriting the default value.

        :return: bool
        """
        return self.active

    def get_auth_token(self):
        """
        Return the user's auth token. Use their password as part of the token
        because if the user changes their password we will want to invalidate
        all of their logins across devices. It is completely fine to use
        md5 here as nothing leaks.

        This satisfies Flask-Login by providing a means to create a token.

        :return: str
        """
        private_key = current_app.config['SECRET_KEY']

        serializer = URLSafeTimedSerializer(private_key)
        data = [str(self.id), md5(self.password.encode('utf-8')).hexdigest()]

        return serializer.dumps(data)

    def authenticated(self, with_password=True, password=''):
        """
        Ensure a user is authenticated, and optionally check their password.

        :param with_password: Optionally check their password
        :type with_password: bool
        :param password: Optionally verify this as their password
        :type password: str
        :return: bool
        """
        if with_password:
            return check_password_hash(self.password, password)

        return True

    def serialize_token(self, expiration=3600):
        """
        Sign and create a token that can be used for things such as resetting
        a password or other tasks that involve a one off token.

        :param expiration: Seconds until it expires, defaults to 1 hour
        :type expiration: int
        :return: JSON
        """
        private_key = current_app.config['SECRET_KEY']

        serializer = TimedJSONWebSignatureSerializer(private_key, expiration)
        return serializer.dumps({'user_email': self.email}).decode('utf-8')

    def update_activity_tracking(self, ip_address):
        """
        Update various fields on the user that's related to meta data on their
        account, such as the sign in count and ip address, etc..

        :param ip_address: IP address
        :type ip_address: str
        :return: SQLAlchemy commit results
        """
        self.sign_in_count += 1

        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_on = datetime.utcnow()
        self.current_sign_in_ip = ip_address

        db.session.add(self)

    def serialize(self):
        d = Serializer.serialize(self)
        del d['password']
        return d


class Application_details(UserMixin, db.Model, Serializer):
    __tablename__ = "application_details"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(10))
    last_name = db.Column(db.String(10))
    current_address = db.Column(db.String(255), nullable=False)
    street_address = db.Column(db.String(255))
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    pin_code = db.Column(db.String(255))
    email = db.Column(db.String(50), nullable=False)
    mobile_number = db.Column(db.String(10), nullable=False)
    position = db.Column(db.String(60), nullable=False)
    status = db.Column(db.Boolean, default=False)
    submitted_on = db.Column(db.DateTime(), default=datetime.utcnow)

    @classmethod
    def get_details(cls, email, mobile_number):
        print(email, mobile_number)
        query = db.session.query(Application_details).filter(Application_details.status == 0)
        if email is None:
            query = query.filter(Application_details.mobile_number == mobile_number).first()
        elif mobile_number is None:
            query = query.filter(Application_details.email == email).first()
        else:
            query = query.filter(Application_details.mobile_number == mobile_number,
                                 Application_details.email == email).first()
        return query

    @classmethod
    def get_row(cls, table_id):
        return Application_details.query.filter(Application_details.id == table_id).first()
