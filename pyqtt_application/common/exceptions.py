class PyQTTException(Exception):
    """
    Base exception for inheritance purposes and general purposes.
    """


class PyQTTDecodeError(PyQTTException):
    """
    Exception use when an error occurs trying to decode data.
    """


class PyQTTInvalidCredentialsError(PyQTTException):
    """
    Exception used when invalid credentials are provided.
    """


class PyQTTTokenError(PyQTTException):
    """
    Exception used when the token is within the token blacklist
    """
