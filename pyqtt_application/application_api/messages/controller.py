"""
All logic related to messages operation so this is executed
outside of the routes definition.
"""
from pyqtt_application.extensions import db
from pyqtt_application.models.messages_models import Message


class MessageController:

    @staticmethod
    def get_message(message_id: int) -> Message:
        """Retrieve a message by its id.

        Args:
            message_id: Message id on the database.

        Returns:
            Message object.
        """
        message = db.session.query(Message).filter_by(id=message_id).first()

        return message

    @staticmethod
    def get_messages(amount: int = 100) -> list:
        """Return a list with a given `amount` of messages.

        Args:
            amount: Number of items to retrieve.

        Returns:
            List with Message objects.
        """
        messages = db.session.query(Message).order_by(Message.id.desc()).limit(amount).all()

        return messages

    @staticmethod
    def get_last_message() -> Message:
        """Return the last message on the database.

        Get latest message by ordering the message by id in descendant order.

        Returns:
             Message object.
        """
        message = db.session.query(Message).order_by(Message.id.desc()).first()

        return message

    @staticmethod
    def delete_message(message_id: int):
        """Delete message by a given id.

        Args:
            message_id: Message id on the database.

        """
        message = Message.query.filter_by(id=message_id).first()
        db.session.delete(message)
        db.session.commit()
