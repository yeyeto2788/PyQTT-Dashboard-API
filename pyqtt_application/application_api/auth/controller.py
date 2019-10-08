from flask import Response

from pyqtt_application.common import exceptions
from pyqtt_application.common.http_responses import HTTPResponse
from pyqtt_application.extensions import db
from pyqtt_application.models.tokenblacklist_models import BlacklistToken
from pyqtt_application.models.users_models import User


def save_token(token: str) -> BlacklistToken or Response:
    """Simple function to store a token into the blacklist.

    Args:
        token: token to be stored on database.

    Returns:
        BlacklistToken when successfully added into the database otherwise
        a flask.Response will be return.
    """
    blacklist_token = BlacklistToken(token=token)

    try:
        # insert the token
        db.session.add(blacklist_token)
        db.session.commit()

        return blacklist_token

    except Exception:

        return HTTPResponse.http_500_unexpected()


class AuthController:
    """Main controller for authorization purposes.

    Methods:
          login_user:
          logout_user:
          get_user_by_token: with a given token get the user from database.
    """

    @staticmethod
    def login_user(data):
        """Check the user is on our database.

        This method will check that the user is on our database by its email and
        password. If the user is on the database, it will generate the token.

        Args:
            data: Request data.

        Returns:
            String with token to be serialized and return to client, otherwise
            a flask.Response will be returned.
        """

        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get("email")).first()

            if user and user.check_password(data.get("password")):
                auth_token = User.encode_auth_token(user.public_id)

                if auth_token:
                    # Added the JWT string at the beginning for easier copy & paste
                    return f"JWT {auth_token.decode('utf-8')}"

            else:

                return HTTPResponse.http_401_unauthorized()

        except Exception:

            return HTTPResponse.http_500_unexpected()

    @staticmethod
    def logout_user(data):
        """Save token given to the user into the blacklist_token table.

        Args:
            data: Request data.

        Returns:
            String with user's public id to be serialized and return to client, otherwise
            a flask.Response will be returned.
        """

        if data:
            auth_token = data.split(" ")[1]

        else:
            auth_token = ""

        if auth_token:

            try:

                resp = User.decode_auth_token(auth_token)

            except exceptions.PyQTTTokenError:

                return HTTPResponse.http_401_unauthorized()

            else:

                if not isinstance(resp, str):
                    # mark the token as blacklisted
                    return save_token(token=auth_token)

                else:

                    return HTTPResponse.http_401_unauthorized()

        else:

            return HTTPResponse.http_403_forbidden()

    @staticmethod
    def get_user_by_token(data) -> User or Response:
        """Decode token and get the user from database decoding the token.

        Args:
            data: Request data.

        Returns:
            User object or flask.Response.
        """
        # get the auth token
        auth_token = data.headers.get("Authorization")

        if auth_token:

            try:

                public_id = User.decode_auth_token(auth_token)

            except Exception:

                return HTTPResponse.http_401_unauthorized()

            else:

                if not isinstance(public_id, str):
                    user_object = User.query.filter_by(
                        public_id=public_id
                    ).first()
                    return user_object

        else:

            return HTTPResponse.http_401_unauthorized(
                message="Provide a valid auth token."
            )
