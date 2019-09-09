"""
Messages model for the database and the operations that can be done
with the Message object.
"""
from collections import OrderedDict
from datetime import datetime

from pyqtt_application.extensions import db


class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    message = db.Column(db.String)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    client = db.Column(db.String)
    user_data = db.Column(db.String)

    def __repr__(self):
        return '<Message:  %r>' % self.message

    def serialize(self):
        serialized = OrderedDict()
        serialized['id'] = self.id
        serialized['topic'] = self.topic
        serialized['message'] = self.message
        serialized['datetime'] = self.datetime
        serialized['timestamp'] = datetime.timestamp(self.datetime)
        serialized['client'] = self.client
        serialized['user_data'] = self.user_data

        return serialized
