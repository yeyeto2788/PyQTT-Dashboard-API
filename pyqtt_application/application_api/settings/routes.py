from flask import request

from pyqtt_application.app_tasks.common_tasks import stop_task
from pyqtt_application.app_tasks.mqtt_tasks import start_recording
from pyqtt_application.application_api.settings import SETTINGS_NS
from pyqtt_application.application_api.settings.schema import SettingsSchema
from pyqtt_application.common.base_routes import BaseResource
from pyqtt_application.extensions import jwt_required


@SETTINGS_NS.route('/record')
class RecordMessages(BaseResource):
    """Start recording messages from a given MQTT broker.

    """
    namespace = SETTINGS_NS
    schema = SettingsSchema()
    parser = schema.parser(method='post')

    @jwt_required()
    @namespace.doc(schema.model_name)
    @namespace.doc(security='swagger_api_key')
    @namespace.expect(parser, validate=True)
    @namespace.response(code=200, description='Success.')
    @namespace.response(code=404, description='No content response.')
    @namespace.response(code=400, description='Unexpected error.')
    def post(self):
        """Resource for subscribing to different topics and brokers.

        """
        arguments = request.args

        host = arguments.get('host', 'test.mosquitto.org')
        port = arguments.get('port', 1883)
        topic = arguments.get('topic', '/#')

        record_options = dict(
            host=host,
            port=port,
            topic=topic
        )

        task = start_recording.apply_async(kwargs=record_options)

        return task.id, 200


@SETTINGS_NS.route('/stop/<string:task_id>')
class StopTasks(BaseResource):
    """Stop task running

    """
    namespace = SETTINGS_NS
    schema = SettingsSchema()

    @jwt_required()
    @namespace.doc(schema.model_name)
    @namespace.doc(security='swagger_api_key')
    @namespace.response(code=200, description='Success.')
    @namespace.response(code=404, description='No content response.')
    @namespace.response(code=400, description='Unexpected error.')
    def post(self, task_id):
        task_arguments = dict(
            task_id=task_id,
        )

        stop_task.apply_async(kwargs=task_arguments)

        return 'OK', 200
