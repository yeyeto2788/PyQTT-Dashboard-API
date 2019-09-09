"""
Extensions module.

Each extension is initialized in the app factory located in app.py.
"""

from flask_sqlalchemy import SQLAlchemy

from flask_restplus import Api

# API basic setup.
api = Api(
    title='MQTT logger and viewer',
    version='0.1',
    description='Python MQTT logger and viewer',
    doc='/docs',
    prefix='/api/v1'
)
# Database
db = SQLAlchemy()
