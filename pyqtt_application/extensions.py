"""
Extensions module.

Each extension is initialized in the app factory located in app.py.
"""
from celery import Celery
from flask_jwt import JWT, jwt_required
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

from pyqtt_application.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        "pyqtt_application.app_tasks.mqtt_tasks",
        "pyqtt_application.app_tasks.common_tasks",
    ],
)

authorizations = {
    "swagger_api_key": {
        "type": "apiKey",
        "in": "header",
        "name": "authorization",
    }
}

# API basic setup.
api = Api(
    title="MQTT logger and viewer",
    version="0.1",
    description="Python MQTT logger and viewer",
    doc="/docs",
    prefix="/api/v1",
    ordered=True,
    authorizations=authorizations,
)

# Database
db = SQLAlchemy()

# JSON web tokens
jwt = JWT()
