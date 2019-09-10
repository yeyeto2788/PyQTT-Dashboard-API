"""
Schema to be return and parameters needed for the different HTTP
verbs available on the routes of the message namespace.
"""
from flask_restplus import fields

from pyqtt_application.application_api.messages import MESSAGE_NS
from pyqtt_application.common.base_schema import BaseSchema


class MessageSchema(BaseSchema):
    """Message schema that should be return on operations.

    """
    model_name = 'Message operations'

    model = MESSAGE_NS.model(
        name='Message',
        model={
            'id': fields.Integer(),
            'topic': fields.String(),
            'message': fields.String(),
            'datetime': fields.DateTime(),
            'client': fields.String(),
            'user_data': fields.String(),
        },
    )

    get_params = {
        'message_id': dict(
            type=fields.Integer(),
            help="Id of the message to retrieve (If -1 will return last).")
    }

    delete_params = {
        'message_id': dict(
            type=fields.Integer(),
            help="Id of the message to delete.")
    }

    post_params = {
        'id': dict(
            type=fields.Integer(),
            help="Id of the message to be added."
        ),
        'topic': dict(
            type=fields.String(),
            help="Topic to be added."
        ),
        'message': dict(
            type=fields.String(),
            help="Message."
        ),
    }
