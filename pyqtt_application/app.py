"""

"""
from flask import Flask

from pyqtt_application.application_api.auth.routes import AUTH_NS
from pyqtt_application.application_api.messages.routes import MESSAGE_NS
from pyqtt_application.application_api.users.routes import USER_NS
from pyqtt_application.extensions import db, api
from pyqtt_application.web_application.messages.messages_blueprint import message_bp
from pyqtt_application.web_application.settings.setting_blueprint import settings_bp


def create_app() -> Flask:
    """Creation of the Flask.app object as factory method.

    More info, here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    Returns:
        app: a Flask app already configured to run.
    """
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    configure_blueprints(app)
    configure_database(app)
    configure_api(app)

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
