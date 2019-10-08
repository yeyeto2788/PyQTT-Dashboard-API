"""
Blueprint for setting purposes so the user can easily change them
as he/she likes.
"""
from flask import Blueprint, jsonify

from pyqtt_application.models.setting_models import Settings

settings_bp = Blueprint(
    name="settings", import_name=__name__, template_folder="templates"
)


@settings_bp.route("/", methods=["GET"])
def root():
    """Get the basic setting already setup on the database.

    """
    settings_obj = Settings.query.all()

    serialized_messages = dict()

    for index, message in enumerate(settings_obj):
        serialized_messages[index] = message.serialize()

    return jsonify(serialized_messages)
