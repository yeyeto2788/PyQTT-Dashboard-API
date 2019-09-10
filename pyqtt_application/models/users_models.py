import datetime

import flask_bcrypt
import jwt

from pyqtt_application.extensions import db
from pyqtt_application.models.tokenblacklist_models import BlacklistToken


class User(db.Model):
    """User Model for storing user related details

    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    @property
    def password(self):
        """Password property write-only access.

        This property should always be write-only since we don't want our application to
        get the actual password.

        Raises:
            AttributeError
        """
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password: str):
        """Generate the hash from a given password.

        Args:
            password:

        """
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):
        """Generates the Auth Token

        Returns:

        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(payload, key, algorithm='HS256')

        except Exception as exec_error:

            return exec_error

    @staticmethod
    def decode_auth_token(auth_token) -> int or str:
        """Decodes the auth token

        Returns:

        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)

            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'

            else:
                return payload['sub']

        except jwt.ExpiredSignatureError:

            return 'Signature expired. Please log in again.'

        except jwt.InvalidTokenError:

            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<{class_name} '{user}'>".format(
            class_name=self.__class__.__name__,
            user=self.username,
        )
