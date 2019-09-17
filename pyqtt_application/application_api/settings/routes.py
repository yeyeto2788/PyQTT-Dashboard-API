from flask import request, Response

from pyqtt_application.application_api.settings import SETTINGS_NS
from pyqtt_application.common.base_routes import BaseResource
from pyqtt_application.application_api.settings.schema import SettingsSchema
from pyqtt_application.common.http_responses import HTTPResponse
from pyqtt_application.app_tasks.mqtt_tasks import start_recording
from pyqtt_application.app_tasks.common_tasks import stop_task


@SETTINGS_NS.route('/record')
class RecordMessages(BaseResource):
    """Start recording messages from MQTT broker.

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


@SETTINGS_NS.route('/stop/<task_id>')
class StopTasks(BaseResource):
    """Stop task running

    """
    namespace = SETTINGS_NS
    schema = SettingsSchema()

    @namespace.doc(schema.model_name)
    @namespace.response(code=200, description='Success.')
    @namespace.response(code=404, description='No content response.')
    @namespace.response(code=400, description='Unexpected error.')
    def post(self, task_id):
        stop_task.apply_async(args=dict(task_id=task_id))

        return 'OK', 200
