from flask import request, Response

from pyqtt_application.application_api.settings import SETTINGS_NS
from pyqtt_application.common.base_routes import BaseResource
from pyqtt_application.application_api.settings.schema import SettingsSchema
from pyqtt_application.common.http_responses import HTTPResponse
from pyqtt_application.tasks.mqtt_tasks import start_recording


@SETTINGS_NS.route('/record')
class RecordMessages(BaseResource):
    """User Login Resource

    """
    namespace = SETTINGS_NS
    schema = SettingsSchema()

    @namespace.doc(schema.model_name)
    @namespace.response(code=200, description='Success.')
    @namespace.response(code=404, description='No content response.')
    @namespace.response(code=400, description='Unexpected error.')
    def post(self):
        record_options = dict(
            host='test.mosquitto.org',
            port=1883,
            topic='/#'
        )

        task = start_recording.apply_async(kwargs=record_options)

        return task.id, 200
