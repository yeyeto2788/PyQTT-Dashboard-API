from flask_restplus import fields

from pyqtt_application.application_api.settings import SETTINGS_NS
from pyqtt_application.common.base_schema import BaseSchema


class SettingsSchema(BaseSchema):
    model_name = "Authentication operations."

    model = SETTINGS_NS.model(
        name='Settings',
        model={}
    )