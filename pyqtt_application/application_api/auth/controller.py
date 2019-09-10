from pyqtt_application.common.http_responses import HTTPResponse
from pyqtt_application.extensions import db
from pyqtt_application.models.tokenblacklist_models import BlacklistToken
from pyqtt_application.models.users_models import User


def save_token(token):
    blacklist_token = BlacklistToken(token=token)

    try:
        # insert the token
        db.session.add(blacklist_token)
        db.session.commit()

        return blacklist_token

    except Exception:

        return HTTPResponse.http_500_unexpected()


class AuthController:

    @staticmethod
    def login_user(data):

        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()

            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.id)

                if auth_token:
                    return auth_token

            else:

                return HTTPResponse.http_401_unauthorized()

        except Exception:

            return HTTPResponse.http_500_unexpected()

    @staticmethod
    def logout_user(data):

        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            resp = User.decode_auth_token(auth_token)

            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)

            else:
                return HTTPResponse.http_401_unauthorized()

        else:
            return HTTPResponse.http_403_forbidden()

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')

        if auth_token:
            resp = User.decode_auth_token(auth_token)

            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }

                return response_object, 200

            response_object = {
                'status': 'fail',
                'message': resp
            }

            return response_object, 401

        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
