"""
Settings namespace use for doing operations through the API.
"""
from flask_restplus import Namespace

SETTINGS_NS = Namespace(
    name='settings',
    description='Settings operations.',
)
