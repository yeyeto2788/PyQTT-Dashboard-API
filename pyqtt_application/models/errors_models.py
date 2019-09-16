"""
Error models for the database so the errors occurred on the application
can be insert into the db.
"""
from collections import OrderedDict
from datetime import datetime

from pyqtt_application.extensions import db


class Errors(db.Model):
    __tablename__ = 'error'

    id = db.Column(db.Integer, primary_key=True)
    error_type = db.column(db.String)
    message = db.column(db.String)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<{class_name}:  {error}>'.format(
            class_name=self.__class__.__name__,
            error=self.message
        )

    def serialize(self):
        serialized = OrderedDict()
        serialized['id'] = self.id
        serialized['message'] = self.message
        serialized['error type'] = self.error_type
        serialized['datetime'] = self.datetime

        return serialized
