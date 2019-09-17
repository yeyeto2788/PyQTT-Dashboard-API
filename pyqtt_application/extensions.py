"""
Extensions module.

Each extension is initialized in the app factory located in app.py.
"""
import flask
from celery import Celery
from flask_jwt import JWT, jwt_required
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

from pyqtt_application.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


class FlaskCelery(Celery):
    """
    Class to handle application teardown and set up on a per-task basis,
    based on the pattern described on http://flask.pocoo.org/docs/1.0/patterns/celery/
    """

    def __init__(self, *args, **kwargs):

        super(FlaskCelery, self).__init__(*args, **kwargs)
        self.patch_task()

        if 'app' in kwargs:
            self.init_app(kwargs['app'])

    def patch_task(self):
        TaskBase = self.Task
        _celery = self

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                if flask.has_app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
                else:
                    with _celery.app.app_context():
                        return TaskBase.__call__(self, *args, **kwargs)

        self.Task = ContextTask

    def init_app(self, app):
        self.app = app
        self.config_from_object(app.config)


celery = FlaskCelery(
    "pyqtt_app_celery",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['pyqtt_application.app_tasks.mqtt_tasks'])

# API basic setup.
api = Api(
    title='MQTT logger and viewer',
    version='0.1',
    description='Python MQTT logger and viewer',
    doc='/docs',
    prefix='/api/v1',
    ordered=True
)

# Database
db = SQLAlchemy()

# JSON web tokens
jwt = JWT()
