"""
Base Resource
"""
import sys
import traceback

from flask import jsonify
from flask_restplus import Resource, marshal


class BaseResource(Resource):
    """
    Class Base for all controllers

    class BaseResource has a set of class attributes set by default to None which are assigned
    to a value after through a child class. Thus every Resource can manage easily and dynamically
    its own controllers, namespace or schema.

    """

    controller_type = None
    namespace = None
    schema = None

    def __init__(self, *args, **kwargs):
        """__init__ method. It calls the supper and set new attributes after.

        Attributes:
            _controller: instance of the controller class of the resource
            namespace: namespace used to route.
            _model: Model object from flask_restplus package defined as the model for the resource.
            If no model defined in child schema classes, it will load the error_model.
            defined in BaseSchema class.
            _error_model = Model object from flask_restplus package defined as the error_model for
            the resource. If no model defined in child schema classes, it will load the error_model
            defined in BaseSchema class.
            _schema: class that contains models schemas used by the API.
            _parser: parser class specified in the schema class.
        """

        super().__init__(*args, **kwargs)
        self._controller = self.controller_type

        self.namespace.model(self.schema.model_name, self.schema.model)
        self.namespace.model(self.schema.error_name, self.schema.error_model)

        self._model = self.namespace.models.get(self.schema.model_name)
        self._error_model = self.namespace.models.get(self.schema.error_name)

        self._schema = self.schema
        self._parser = self._schema.parser

    @staticmethod
    def _unexpected_response():
        """
        This method should be called when unexpected exception occurs during the execution.

        Returns: dict with the exception information:
            {
                'type': 'ExceptionType'
                'error': 'ExceptionString'
                'stack_trace': 'StackTrace'
            }
        """

        exc_type, exc_value, exc_traceback = sys.exc_info()
        trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
        res = dict(
            type=repr(exc_type),
            error=repr(exc_value),
            stack_trace=repr(trace),
        )

        return jsonify(res)

    @staticmethod
    def _ok_response(obj, model):
        """
        This method should be called wherever the API gives a 200 code HTTP Response.

        Args:
            obj (dict): dict that contains data to be encapsulated by an API Model.
            model (dict): Fields description of data in obj in order to build the API Model.

        Returns:
            tuple: a tuple that contains an OrderedDict to build the json in the HTTP response and
            the HTTP code which is 200.
        """

        return marshal(obj, model), 200

    @staticmethod
    def _no_content_response():
        """
        This method should be called wherever the API gives a 204 code HTTP Response.

        Returns:
            tuple: a tuple that contains an empty string (since there's no content) and
            the HTTP code which is 204.
        """

        return '', 204

    @staticmethod
    def _not_found_response(item_name=None, msg=None):
        """
        This method should be called wherever the API gives a 404 code HTTP Response.

        Args:
            item_name (str, optional): name of the item. Defaults to None. If None then item_name
            value will be 'Item'.
            msg (str, optional): message to show in the response. Defaults to None. If None then
            value will be '{item_name} requested was not found'.

        Returns:
            tuple: a tuple that contains a message and the HTTP code which is 404.
        """

        item_name = item_name or 'Item'
        msg = msg or f'{item_name} requested was not found'
        return msg, 404
