"""
Extensions module.

Each extension is initialized in the app factory located in app.py.
"""

from flask_jwt import JWT, jwt_required
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

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
jwt = JWT()
celery = Celery(include=['pyqtt_application.tasks.mqtt_tasks'])
