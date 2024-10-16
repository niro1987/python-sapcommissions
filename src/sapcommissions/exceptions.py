"""Exceptions for Python SAP Commissions Client."""

from typing import Any


class SAPException(Exception):
    """Base exception for Python SAP Commissions Client."""


class SAPConnectionError(SAPException):
    """Exception to indicate connection error."""


class SAPResponseError(SAPException):
    """Exception to indicate an unexpected response."""


class SAPBadRequest(SAPException):
    """Exception to indicate an error with the request."""

    def __init__(self, message: str, data: dict[str, Any]) -> None:
        """Initialize a Bad Request exception."""
        self.data = data
        super().__init__(message, {"data": data})


class SAPNotModified(SAPException):
    """Exception to indicate 304 - Not Modified response."""


class SAPAlreadyExists(SAPException):
    """Exception to indicate resource with same key already exists."""


class SAPMissingField(SAPException):
    """Exception to indicate one or more required fields are missing."""

    def __init__(self, fields: dict[str, Any]) -> None:
        """Initialize a Missing Required Field exception."""
        self.fields = fields
        super().__init__("Missing Required Field(s)", {"fields": fields})


class SAPNotFound(SAPException):
    """Exception to indicate resource does not exist."""
