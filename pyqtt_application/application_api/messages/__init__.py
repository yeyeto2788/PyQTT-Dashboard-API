"""
Messages namespace use for doing operations through the API.
"""
from flask_restplus import Namespace

MESSAGE_NS = Namespace(
    name='api_messages',
    description='Messages operations.',
)
