import sys
import traceback
from datetime import datetime

from flask import jsonify, make_response
from flask_restplus import marshal


class BaseResponse:
    """
    Base response object to be used as serializable object when making
    http responses.
    """
    data: str = ''
    code: int = 0
    timestamp: int = 0
    status: str = ''
    errors: None


class HTTPResponse:

    @staticmethod
    def http_response(data=None, code=None, status=None, errors=None):
        response = BaseResponse()
        response.data = data
        response.code = code
        response.status = status
        response.errors = errors
        response.timestamp = datetime.timestamp(datetime.now())

        return make_response(jsonify(response.__dict__), response.code)

    @staticmethod
    def http_200_ok(data, model):
        data = marshal(data, model)
        code = 200
        status = 'Success.'

        return HTTPResponse.http_response(data=data, code=code, status=status)

    @staticmethod
    def http_201_created(item_name=None, message=None):
        item_name = item_name or 'Item'
        message = message or f'{item_name} added.'

        data = dict(
            message=message
        )
        code = 201
        status = 'Success.'

        return HTTPResponse.http_response(data=data, code=code, status=status)

    @staticmethod
    def http_204_no_content():
        data = 'No content'
        code = 204

        return HTTPResponse.http_response(data, code)

    @staticmethod
    def http_401_unauthorized(message=None):
        message = message or 'Login failed, check you credentials'

        data = dict(
            message=message
        )
        code = 401
        status = 'Fail.'

        return HTTPResponse.http_response(data=data, code=code, status=status)

    @staticmethod
    def http_403_forbidden():
        message = 'Provide a valid auth token.'

        data = dict(
            message=message
        )
        code = 403
        status = 'Fail.'

        return HTTPResponse.http_response(data=data, code=code, status=status)

    @staticmethod
    def http_404_not_found(item_name=None, message=None):
        item_name = item_name or 'Item'
        message = message or f'{item_name} requested was not found'

        data = dict(
            message=message
        )
        code = 404
        status = 'Fail.'

        return HTTPResponse.http_response(data=data, code=code, status=status)

    @staticmethod
    def http_409_already_exists(item_name=None, message=None):
        item_name = item_name or 'Item'
        message = message or f'{item_name} already exists'

        data = dict(
            message=message
        )
        code = 409
        status = 'Fail.'

        return HTTPResponse.http_response(data=data, code=code, status=status)

    @staticmethod
    def http_500_unexpected():
        exc_type, exc_value, exc_traceback = sys.exc_info()
        trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
        error = dict(
            type=repr(exc_type),
            error=repr(exc_value),
            stack_trace=repr(trace),
        )

        code = 500
        status = 'Fail.'

        return HTTPResponse.http_response(errors=error, code=code, status=status)
