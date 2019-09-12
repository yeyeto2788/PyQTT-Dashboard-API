"""
Messages model for the database and the operations that can be done
with the Message object.
"""
from collections import OrderedDict
from datetime import datetime

from pyqtt_application.extensions import db


class Message(db.Model):
    """
    Message representation on database and useful methods for
    message handling operations.
    """
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    message = db.Column(db.String)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    client = db.Column(db.String)
    user_data = db.Column(db.String)

    def __repr__(self):
        return '<{class_name}:  {message}>'.format(
            class_name=self.__class__.__name__,
            message=self.message
        )

    def serialize(self) -> OrderedDict:
        """Make the Message object into a serializable object.

        Returns:
            OrderedDict
        """
        serialized = OrderedDict()
        serialized['id'] = self.id
        serialized['topic'] = self.topic
        serialized['message'] = self.message
        serialized['datetime'] = self.datetime
        serialized['timestamp'] = datetime.timestamp(self.datetime)
        serialized['client'] = self.client
        serialized['user_data'] = self.user_data

        return serialized
