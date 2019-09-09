"""
Authentication namespace use for doing operations through the API.
"""
from flask_restplus import Namespace

AUTH_NS = Namespace(
    name='api_auth',
    description='Authentication operations.',
)
