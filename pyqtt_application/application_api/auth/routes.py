from pyqtt_application.application_api.auth import AUTH_NS
from pyqtt_application.application_api.auth.controller import AuthController
from pyqtt_application.common.base_routes import BaseResource
from pyqtt_application.application_api.auth.schema import AuthSchema


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
        # TODO: get the post data
        data = dict(
            email="test@test.com",
            password="1234"
        )
        response = AuthController.login_user(data)
        return response


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
        # TODO: get auth token
        data = dict(
            email="test@test.com",
            password="1234"
        )
        response = AuthController.logout_user(data)
        return 200, response
