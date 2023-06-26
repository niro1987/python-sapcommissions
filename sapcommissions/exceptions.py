"""
Exceptions for the sapcommissions package.
"""


class ClientError(Exception):
    """Exception that incdicates that there was an error with the client."""


class ServerError(Exception):
    """Exception that incdicates that there was an error with the server."""


class AuthenticationError(ClientError):
    """
    User is not authorized to perform the request. Likely due to an incorrect
    username, password or missing privileges.
    """
