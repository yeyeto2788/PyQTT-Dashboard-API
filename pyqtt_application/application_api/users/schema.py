from flask_restplus import fields

from pyqtt_application.application_api.users import USER_NS
from pyqtt_application.common.base_schema import BaseSchema


class UserSchema(BaseSchema):
    model_name = "User operations"

    model = USER_NS.model(
        name='User',
        model={
            'email': fields.String(),
            'username': fields.String(),
            'pasword': fields.String(),
            'public_id': fields.String(),
        },
    )

    post_params = {
        'email': dict(
            type=fields.String(),
            help="User's email.",
        ),
        'username': dict(
            type=fields.String(),
            help="Username.",
        ),
        'password': dict(
            type=fields.String(),
            help="User's password.",
        ),
    }

    delete_params = {}

    put_params = {
        'public_id': dict(
            type=fields.String(),
            help="User's' public id.",
        ),
        'password': dict(
            type=fields.String(),
            help="User's password.",
        ),
    }
