"""
Base schema used all over the application.
"""

from flask_restplus import fields, reqparse


class BaseSchema:
    """
    Class Base for all schemas
    """
    model_name: str = 'Model name'
    model = dict()

    error_name: str = 'Errors'
    error_model: dict = {
        'type': fields.String,
        'error': fields.String,
        'stack_trace': fields.String,
    }

    base_params = dict()

    def parser(self, method: str = 'get') -> reqparse.RequestParser:
        """
        This method retrieve the query string arguments sent to the endpoint

        Args:
            method: method to match with the model. Defaults to 'get'.

        Returns:
            flask_restplus.reqparse.RequestParser
        """
        parser = reqparse.RequestParser()
        method = method.lower()

        base_params = dict(self.base_params)
        method_params = getattr(self, f'{method}_params', {})
        params_names = method_params.keys() | base_params.keys()

        for name in params_names:
            method_param_value = method_params.get(name, None)

            if method_param_value:
                base_params[name] = method_param_value

            parsed_arg = base_params.get(name)

            parser.add_argument(name=name, **parsed_arg)

        return parser
