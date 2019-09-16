from datetime import datetime

from pyqtt_application.extensions import db


class Settings(db.Model):
    __tablename__ = 'setting'

    key = db.Column(db.String, primary_key=True)
    value = db.Column(db.String)
    update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<{class_name}:  {broker}>'.format(
            class_name=self.__class__.__name__,
            broker=self.broker
        )

    def serialize(self):
        serialized = dict()
        serialized['key'] = self.key
        serialized['value'] = self.value
        serialized['update'] = self.update

        return serialized
