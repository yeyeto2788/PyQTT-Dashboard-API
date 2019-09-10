from datetime import datetime
import sys
import traceback

from flask import jsonify, make_response
from flask_restplus import marshal


class BaseResponse:
    data: str = ''
    code: int = 0
    timestamp: int = 0
    status: str = ''
    errors: None


class HTTPResponse:

    @staticmethod
    def http_200_ok(data, model):
        response = BaseResponse()
        response.data = marshal(data, model)
        response.code = 200
        response.status = 'Success.'
        response.timestamp = datetime.timestamp(datetime.now())

        return make_response(jsonify(response.__dict__), response.code)

    @staticmethod
    def http_201_created(item_name=None, message=None):
        item_name = item_name or 'Item'
        message = message or f'{item_name} added.'

        response = BaseResponse()
        response.data = dict(
            message=message
        )
        response.code = 201
        response.status = 'Success.'
        response.timestamp = datetime.timestamp(datetime.now())

        return make_response(jsonify(response.__dict__), response.code)

    @staticmethod
    def http_204_no_content():
        response = BaseResponse()
        response.data = 'No content'
        response.code = 204
        response.timestamp = datetime.timestamp(datetime.now())

        return make_response(jsonify(response.__dict__), response.code)

    @staticmethod
    def http_401_unauthorized():
        message = 'Login failed, check you credentials'

        response = BaseResponse()
        response.data = dict(
            message=message
        )
        response.code = 401
        response.status = 'Fail.'
        response.timestamp = datetime.timestamp(datetime.now())

        return make_response(jsonify(response.__dict__), response.code)

    @staticmethod
    def http_403_forbidden():
        message = 'Provide a valid auth token.'

        response = BaseResponse()
        response.data = dict(
            message=message
        )
        response.code = 403
        response.status = 'Fail.'
        response.timestamp = datetime.timestamp(datetime.now())

        return make_response(jsonify(response.__dict__), response.code)

    @staticmethod
    def http_404_not_found(item_name=None, message=None):
        item_name = item_name or 'Item'
        message = message or f'{item_name} requested was not found'

        response = BaseResponse()
        response.data = dict(
            message=message
        )
        response.code = 404
        response.status = 'Fail.'
        response.timestamp = datetime.timestamp(datetime.now())

        return make_response(jsonify(response.__dict__), response.code)

    @staticmethod
    def http_409_already_exists(item_name=None, message=None):
        item_name = item_name or 'Item'
        message = message or f'{item_name} already exists'

        response = BaseResponse()
        response.data = dict(
            message=message
        )
        response.code = 409
        response.status = 'Fail.'
        response.timestamp = datetime.timestamp(datetime.now())

        return make_response(jsonify(response.__dict__), response.code)

    @staticmethod
    def http_500_unexpected():
        exc_type, exc_value, exc_traceback = sys.exc_info()
        trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
        data = dict(
            type=repr(exc_type),
            error=repr(exc_value),
            stack_trace=repr(trace),
        )

        response = BaseResponse()
        response.data = None
        response.code = 500
        response.error = data
        response.status = 'Fail.'
        response.timestamp = datetime.timestamp(datetime.now())

        return make_response(jsonify(response.__dict__), response.code)
