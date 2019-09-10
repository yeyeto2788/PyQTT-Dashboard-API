from flask_restplus import fields

from pyqtt_application.application_api.auth import AUTH_NS
from pyqtt_application.common.base_schema import BaseSchema


class AuthSchema(BaseSchema):
    model_name = "Authentication operations."

    model = AUTH_NS.model(
        name='Auth',
        model={
            'token': fields.String(),
        }
    )

    post_params = {
        'email': dict(
            type=fields.String(),
            help="Public user id."
        ),
        'password': dict(
            type=fields.String(),
            help="User password hash"
        )
    }
