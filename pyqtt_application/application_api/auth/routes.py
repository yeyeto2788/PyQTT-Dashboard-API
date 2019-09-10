from flask import request

from pyqtt_application.application_api.auth import AUTH_NS
from pyqtt_application.application_api.auth.controller import AuthController
from pyqtt_application.application_api.auth.schema import AuthSchema
from pyqtt_application.common.base_routes import BaseResource
from pyqtt_application.common.http_responses import HTTPResponse


@AUTH_NS.route('/login')
class LoginAPI(BaseResource):
    """User Login Resource

    """
    controller_type = AuthController()
    namespace = AUTH_NS
    schema = AuthSchema()
    parser = schema.parser(method='post')

    @namespace.doc(schema.model_name)
    @namespace.expect(parser, validate=True)
    @namespace.response(code=200, description='Success.')
    @namespace.response(code=404, description='No content response.')
    @namespace.response(code=400, description='Unexpected error.')
    def post(self):

        post_data = request.json

        response = AuthController.login_user(post_data)

        if isinstance(response, HTTPResponse):

            return response

        else:
            data = dict(token=response)

            return HTTPResponse.http_200_ok(data=data, model=self._model)


@AUTH_NS.route('/logout')
class LogoutAPI(BaseResource):
    """

    """

    controller_type = AuthController()
    namespace = AUTH_NS
    schema = AuthSchema()
    parser = schema.parser(method='post')

    @namespace.doc(schema.model_name)
    @namespace.expect(parser, validate=True)
    @namespace.response(code=200, description='Success.')
    @namespace.response(code=404, description='No content response.')
    @namespace.response(code=400, description='Unexpected error.')
    def post(self):
        auth_header = request.headers.get('Authorization')

        response = AuthController.logout_user(auth_header)

        if isinstance(response, HTTPResponse):

            return response

        else:
            data = dict(token=response)

            return HTTPResponse.http_200_ok(data=data, model=self._model)
