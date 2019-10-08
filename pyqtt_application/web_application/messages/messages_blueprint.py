"""
Blueprint for the messages operations via web so the routes declared here
should return a template.
"""
from flask import Blueprint, jsonify

from pyqtt_application.extensions import db
from pyqtt_application.models.messages_models import Message

message_bp = Blueprint(
    name="messages", import_name=__name__, template_folder="templates"
)


@message_bp.route("/", methods=["GET"])
def root():
    """

    """
    messages = db.session.query(Message).order_by(Message.id.desc()).limit(100).all()

    serialized_messages = dict()

    for message in reversed(messages):
        serialized_messages[message.id] = message.serialize()

    return jsonify(serialized_messages)
