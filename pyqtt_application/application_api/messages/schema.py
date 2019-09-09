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
        'Message',
        {
            'data':
                {
                    'id': fields.Integer(),
                    'topic': fields.String(),
                    'message': fields.String(),
                    'datetime': fields.DateTime(),
                    'client': fields.String(),
                    'user_data': fields.String(),
                }
        }
    )

    delete_params = {
        'id': fields.Integer()
    }
