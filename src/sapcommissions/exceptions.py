"""Exceptions for Python SAP Commissions Client."""

from typing import Any


class SAPException(Exception):
    """Base exception for Python SAP Commissions Client."""


class SAPConnectionError(SAPException):
    """Exception to indicate connection error."""


class SAPResponseError(SAPException):
    """Exception to indicate an unexpected response."""


class SAPNotModified(SAPException):
    """Exception to indicate 304 - Not Modified response."""


class SAPBadRequest(SAPException):
    """Exception to indicate an error with the request."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize a Bad Request exception."""
        self.data = data
        super().__init__("Bad Request", {"data": data})


class SAPAlreadyExists(SAPException):
    """Exception to indicate resource with same key already exists."""


class SAPMissingField(SAPException):
    """Exception to indicate one or more required fields are missing."""

    def __init__(self, fields: dict[str, Any]) -> None:
        """Initialize a Missing Required Field exception."""
        self.fields = fields
        super().__init__("Missing Required Field(s)", {"fields": fields})


class SAPUnsupportedFileError(SAPException):
    """Exception to indicate file is not supported."""


class RequestError(SAPException):
    """Exception to indicate an error while handling the server request."""


class ResponseError(SAPException):
    """Exception to indicate an error while handling the server response."""


class CRUDError(SAPException):
    """Base Exception for CRUD operations."""


class AlreadyExistsError(CRUDError):
    """Exception to indicate resource with same key already exists."""


class MissingFieldError(CRUDError):
    """Exception to indicate a value is required."""


class PeriodTypeError(CRUDError):
    """Exception to indicate a Period Type mismatch."""


class NotModifiedError(CRUDError):
    """Exception to indicate resource was not modified."""


class NotFoundError(CRUDError):
    """Exception to indicate resource does not exist."""


class ReferredByError(CRUDError):
    """Exception to indicate resource is referred by another resource."""


class DeleteFailedError(CRUDError):
    """Exception to indicate resource was not deleted."""
