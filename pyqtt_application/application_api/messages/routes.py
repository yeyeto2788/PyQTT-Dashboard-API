"""
Routes/endpoints for the messages namespace.
"""
from flask import request

from pyqtt_application.application_api.messages import MESSAGE_NS
from pyqtt_application.application_api.messages.controller import MessageController
from pyqtt_application.application_api.messages.schema import MessageSchema
from pyqtt_application.common.base_routes import BaseResource


@MESSAGE_NS.route("/")
class MessageResource(BaseResource):
    """
    Message operation
    """
    controller_type = MessageController()
    namespace = MESSAGE_NS
    schema = MessageSchema()
    get_parser = schema.parser(method='get')
    delete_parser = schema.parser(method='delete')
    put_parser = schema.parser(method='put')

    @namespace.doc(schema.model_name)
    @namespace.expect(get_parser, validate=True)
    @namespace.response(code=200, description='Success.')
    @namespace.response(code=404, description='No content response.')
    @namespace.response(code=400, description='Unexpected error.')
    def get(self):
        """Retrieve information about a given message by its id.

        """

        try:
            arguments = request.args
            message_id = arguments.get('message_id')

            if message_id == -1:
                message_obj = self.controller_type.get_last_message()
            else:
                message_obj = self.controller_type.get_message(message_id)

            if message_obj:
                response = self._ok_response(message_obj, self._model)

            else:
                response = self._not_found_response(
                    msg=f"Message with id {message_id} was not found.")

        except Exception:
            response = self._unexpected_response()

        return response

    @namespace.doc(schema.model_name)
    @namespace.expect(delete_parser, validate=True)
    @namespace.response(code=200, description='Success')
    @namespace.response(code=400, description='Unexpected error')
    def delete(self):
        """Delete a given message from its id.

        """
        try:
            arguments = request.args
            message_id = arguments['message_id']

            message = self.controller_type.delete_message(message_id)

            return self._ok_response(message, self._model)

        except Exception:
            return self._unexpected_response()

    @namespace.doc(schema.model_name)
    @namespace.expect(put_parser, validate=True)
    @namespace.response(code=200, description='Success')
    @namespace.response(code=400, description='Unexpected error')
    def put(self):
        """Add a message to the database.

        """

        arguments = request.args

        id = arguments['id']
        topic = arguments['topic']
        message = arguments['message']

        try:
            message_obj = self.controller_type.add_message(
                id=id,
                topic=topic,
                message=message
            )

            return self._ok_response(message_obj, self._model)

        except Exception:
            return self._unexpected_response()