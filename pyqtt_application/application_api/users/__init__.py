"""
Users namespace use for doing operations through the API.
"""
from flask_restplus import Namespace

USER_NS = Namespace(
    name='users',
    description='User operations.',
)
