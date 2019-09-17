"""

"""
from flask import Flask
from werkzeug.security import safe_str_cmp

from pyqtt_application.extensions import db, api, jwt, celery
from pyqtt_application.application_api.auth.routes import AUTH_NS
from pyqtt_application.application_api.messages.routes import MESSAGE_NS
from pyqtt_application.application_api.settings.routes import SETTINGS_NS
from pyqtt_application.application_api.users.routes import USER_NS
from pyqtt_application.models.users_models import User
from pyqtt_application.web_application.messages.messages_blueprint import message_bp
from pyqtt_application.web_application.settings.setting_blueprint import settings_bp


def authenticate(username, password):
    """Simple function to authenticate the user on the API

    Args:
        username:
        password:

    Returns:
        User object.
    """
    user = User.query.filter_by(username=username).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    """Check that the public id is the one the database.

    Args:
        payload: Data from the request header.

    Returns:
        User object if found.
    """
    public_id = payload['public_id']
    return User.query.filter_by(public_id=public_id).first()


def create_app() -> Flask:
    """Creation of the Flask.app object as factory method.

    More info, here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    Returns:
        app: a Flask app already configured to run.
    """
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.app_context().push()

    configure_blueprints(app)
    configure_database(app)
    configure_api(app)
    configure_jwt(app)
    configure_celery(app)

    return app


def configure_database(app: Flask):
    """Configuration of the database.

    Args:
        app: a Flask application.
    """
    db.init_app(app)


def configure_blueprints(app: Flask):
    """Registration of the application blueprints.

    Args:
        app: a Flask application.
    """

    app.register_blueprint(message_bp, url_prefix='/messages')
    app.register_blueprint(settings_bp, url_prefix='/settings')


def configure_api(app: Flask):
    """Initialize and configure API

    This will initialize the API and add the namespaces on the
    API.

    Args:
        app: a Flask application.
    """
    # Add namespaces from routes to api
    api.init_app(app)
    api.add_namespace(AUTH_NS, path='/auth')
    api.add_namespace(MESSAGE_NS, path='/messages')
    api.add_namespace(USER_NS, path='/users')
    api.add_namespace(SETTINGS_NS, path='/settings')


def configure_jwt(app):
    """Initialize the jwt module on the application.

    Also set the callback functions for identity and authentication.

    Args:
        app: a Flask application.

    """
    jwt.authentication_callback = authenticate
    jwt.identity_callback = identity
    jwt.init_app(app)


def configure_celery(app: Flask):
    """
    Initialize celery in order to get working the tasks.

    Args:
        app: a Flask application.

    """
    celery.config_from_object(app.config)
