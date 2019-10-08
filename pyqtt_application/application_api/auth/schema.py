from flask_restplus import fields

from pyqtt_application.application_api.auth import AUTH_NS
from pyqtt_application.common.base_schema import BaseSchema


class AuthSchema(BaseSchema):
    model_name = "Authentication operations."

    model = AUTH_NS.model(name="Auth", model={"access_token": fields.String()})

    post_params = {
        "email": dict(type=fields.String(required=True), help="User's email."),
        "password": dict(
            type=fields.String(required=True, format="password"), help="User password."
        ),
    }
