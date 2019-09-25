"""
Routes/endpoints for the messages namespace.
"""
from flask import request, Response

from pyqtt_application.application_api.messages import MESSAGE_NS
from pyqtt_application.application_api.messages.controller import MessageController
from pyqtt_application.application_api.messages.schema import MessageSchema
from pyqtt_application.common.base_routes import BaseResource
from pyqtt_application.common.http_responses import HTTPResponse
from pyqtt_application.extensions import jwt_required


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
    post_parser = schema.parser(method='post')

    @jwt_required()
    @namespace.doc(schema.model_name)
    @namespace.doc(security='swagger_api_key')
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

            if int(message_id) == -1:
                message_obj = self.controller_type.get_last_message()

            else:
                message_obj = self.controller_type.get_message(message_id)

            if message_obj:

                response = HTTPResponse.http_200_ok(message_obj, self._model)

            else:
                response = HTTPResponse.http_404_not_found(
                    message=f"Message with id {message_id} was not found.")

        except Exception:
            response = HTTPResponse.http_500_unexpected()

        return response

    @jwt_required()
    @namespace.doc(schema.model_name)
    @namespace.doc(security='swagger_api_key')
    @namespace.expect(delete_parser, validate=True)
    @namespace.response(code=200, description='Success')
    @namespace.response(code=400, description='Unexpected error')
    def delete(self):
        """Delete a given message from its id.

        """
        try:
            arguments = request.args
            message_id = arguments['message_id']

            operation_return = self.controller_type.delete_message(message_id)

            if isinstance(operation_return, Response):

                return operation_return

            else:

                return HTTPResponse.http_200_ok(operation_return, self._model)

        except Exception:

            return HTTPResponse.http_500_unexpected()

    @jwt_required()
    @namespace.doc(schema.model_name)
    @namespace.doc(security='swagger_api_key')
    @namespace.expect(post_parser, validate=True)
    @namespace.response(code=200, description='Success')
    @namespace.response(code=400, description='Unexpected error')
    def post(self):
        """Add a message to the database.

        """

        arguments = request.args

        message_id = arguments['id']
        topic = arguments['topic']
        message = arguments['message']

        try:
            message_obj = self.controller_type.add_message(
                message_id=message_id,
                topic=topic,
                message=message
            )

            return self._ok_response(message_obj, self._model)

        except Exception:

            return HTTPResponse.http_500_unexpected()
