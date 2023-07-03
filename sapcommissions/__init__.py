"""
A Python wrapper for the SAP Commissions API.
"""
from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True)
class Connection:
    """
    Connection variables used to connect with SAP Commissions.
    """

    tenant: str = field(repr=True)
    environment: str = field(repr=True)
    username: str = field(repr=True)
    password: str = field(repr=False)
    verifySsl: bool = field(default=True, repr=False)

    @property
    def url(self) -> str:
        """Return the Commissions URL."""
        return f"https://{self.tenant}-{self.environment}.callidusondemand.com"

    @property
    def apiUrl(self) -> str:
        """Returns the base url for the Commissions REST API."""
        return self.url + "/api"

    @property
    def apiDocument(self) -> str:
        """Returns the url for the Commissions API documentation."""
        return self.url + "/APIDocument"


class ReportFormat(Enum):
    """
    Enum for the report format.
    """

    PDF = "pdf"
    EXCEL = "excel"
    NATIVE = "native"


class Revalidate(Enum):
    """
    Enum for revalidate mode.
    """

    ALL = "all"
    ONLY_ERRORS = "onlyError"


class ImportRunMode(Enum):
    """
    Enum for import runMode.
    """

    ALL = "all"
    NEW = "new"


class PipelineRunMode(Enum):
    """
    Enum for pipeline runMode.
    """

    FULL = "full"
    INCREMENTAL = "incremental"
