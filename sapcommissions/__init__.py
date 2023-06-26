"""
A Python wrapper for the SAP Commissions API.
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Connection:
    """
    Connection variables used to connect with SAP Commissions.
    """

    tenant: str = field(repr=True)
    environment: str = field(repr=True)
    username: str = field(repr=True)
    password: str = field(repr=False)
    verify_ssl: bool = field(default=True, repr=False)

    @property
    def url(self) -> str:
        """Return the Commissions URL."""
        return f"https://{self.tenant}-{self.environment}.callidusondemand.com"

    @property
    def api_url(self) -> str:
        """Returns the base url for the Commissions REST API."""
        return self.url + "/api"

    @property
    def api_document(self) -> str:
        """Returns the url for the Commissions API documentation."""
        return self.url + "/APIDocument"
