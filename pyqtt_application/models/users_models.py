import datetime

import flask_bcrypt
import jwt

from pyqtt_application.common import exceptions
from pyqtt_application.config import JWT_SECRET_KEY, JWT_ALGORITHM
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
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password: str):
        """Generate the hash from a given password.

        Args:
            password:

        """
        self.password_hash = flask_bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):
        """Generates the Auth Token

        Args:
            user_id:

        Returns:
            Token for the client and authorization operations.
        """
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=1, seconds=5),
                "iat": datetime.datetime.utcnow()
                - datetime.timedelta(seconds=5),
                "nbf": datetime.datetime.utcnow(),
                "public_id": user_id,
            }

            return jwt.encode(
                payload=payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
            )

        except Exception as exec_error:

            return exec_error

    @staticmethod
    def decode_auth_token(auth_token) -> str:
        """Decodes the auth token

        Returns:

        """
        try:
            payload = jwt.decode(
                jwt=auth_token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
            )
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)

            if is_blacklisted_token:
                return "Token blacklisted. Please log in again."

            else:
                return payload["public_id"]

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):

            raise exceptions.PyQTTTokenError

    def __repr__(self):
        return "<{class_name}: '{user}':'{id}'>".format(
            class_name=self.__class__.__name__,
            user=self.username,
            id=self.public_id,
        )
