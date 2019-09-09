"""
Routes/endpoints for the messages namespace.
"""
from pyqtt_application.application_api.messages import MESSAGE_NS
from pyqtt_application.application_api.messages.controller import MessageController
from pyqtt_application.application_api.messages.schema import MessageSchema
from pyqtt_application.common.base_routes import BaseResource


@MESSAGE_NS.route("/<int:message_id>")
class MessageResource(BaseResource):
    """
    Message operation
    """
    controller_type = MessageController()
    namespace = MESSAGE_NS
    schema = MessageSchema()
    parser = schema.parser(method='get')

    @namespace.doc(schema.model_name)
    @namespace.expect(parser, validate=True)
    @namespace.response(code=200, description='Success.')
    @namespace.response(code=404, description='No content response.')
    @namespace.response(code=400, description='Unexpected error.')
    def get(self, message_id):
        """Retrieve information about a given message by its id.

        """
        try:
            messages = self.controller_type.get_message(message_id)

            if messages:
                response = self._ok_response(messages, self._model)

            else:
                response = self._not_found_response(
                    msg=f"Message with id {message_id} was not found.")

        except Exception:
            response = self._unexpected_response()

        return response

    @namespace.doc(schema.model_name)
    @namespace.expect(parser, validate=True)
    @namespace.response(code=200, description='Success')
    @namespace.response(code=400, description='Unexpected error')
    def delete(self, message_id):
        """Delete a given message from its id.

        """
        try:
            message = self.controller_type.delete_message(message_id)

            return self._ok_response(message, self._model)

        except Exception:
            return self._unexpected_response()


@MESSAGE_NS.route("/last")
class LastMessageResource(BaseResource):
    """

    """
    controller_type = MessageController()
    namespace = MESSAGE_NS
    schema = MessageSchema()
    parser = schema.parser(method='get')

    @namespace.doc(schema.model_name)
    @namespace.expect(parser, validate=True)
    @namespace.response(code=200, description='Success')
    @namespace.response(code=400, description='Unexpected error')
    def get(self):
        """Get last message on database.

        """
        try:
            message = self.controller_type.get_last_message()

            return self._ok_response(message, self._model)

        except Exception:
            return self._unexpected_response()
