from flask_restplus import fields

from pyqtt_application.application_api.settings import SETTINGS_NS
from pyqtt_application.common.base_schema import BaseSchema


class SettingsSchema(BaseSchema):
    model_name = "Authentication operations."

    model = SETTINGS_NS.model(name="Settings", model={})

    post_params = {
        "host": dict(
            type=fields.String(),
            help="Host to listen to.",
            default="broker.hivemq.com",
        ),
        "port": dict(
            type=fields.String(),
            help="Open on which the broker is.",
            default=1883,
        ),
        "topic": dict(
            type=fields.String(), help="Topic to subscribe to.", default="/#"
        ),
    }
