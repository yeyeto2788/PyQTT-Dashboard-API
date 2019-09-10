from flask import request

from pyqtt_application.application_api.users import USER_NS
from pyqtt_application.application_api.users.controller import UserController
from pyqtt_application.application_api.users.schema import UserSchema
from pyqtt_application.common.base_routes import BaseResource
from pyqtt_application.common.http_responses import HTTPResponse


@USER_NS.route("/")
class UserResource(BaseResource):
    """
    Message operation
    """
    controller_type = UserController()
    namespace = USER_NS
    schema = UserSchema()
    put_parser = schema.parser(method='put')
    delete_parser = schema.parser(method='delete')
    post_parser = schema.parser(method='post')

    @namespace.doc(schema.model_name)
    @namespace.expect(post_parser, validate=True)
    @namespace.response(code=200, description='Success')
    @namespace.response(code=400, description='Unexpected error')
    def post(self):

        arguments = request.args

        email = arguments['email']
        username = arguments['username']
        password = arguments['password']

        try:
            response = self.controller_type.add_user(
                email=email,
                username=username,
                password=password
            )

            return response

        except Exception:

            return HTTPResponse.http_500_unexpected()

    @namespace.doc(schema.model_name)
    @namespace.expect(put_parser, validate=True)
    @namespace.response(code=200, description='Success')
    @namespace.response(code=400, description='Unexpected error')
    def put(self):

        try:
            arguments = request.args
            user_id = arguments['public_id']
            new_password = arguments['password']

            user_obj = self.controller_type.edit_user_password(
                public_id=user_id, password=new_password
            )

            return HTTPResponse.http_200_ok(user_obj, self._model)

        except Exception:

            return HTTPResponse.http_500_unexpected()
