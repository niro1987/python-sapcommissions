"""Config for Pytest."""

from collections.abc import AsyncGenerator

import pytest
from aiohttp import BasicAuth, ClientSession
from dotenv import dotenv_values

from sapcommissions import CommissionsClient


@pytest.fixture(name="config")
def fixture_config() -> dict[str, str]:
    """Return the configuration values from the .env file."""
    return dotenv_values("tests/.env")


@pytest.fixture(name="session")
async def fixture_session(
    config: dict[str, str],
) -> AsyncGenerator[ClientSession, None]:
    """Yield an async client session."""
    username: str = config["SAP_USERNAME"]
    password: str = config["SAP_PASSWORD"]
    auth: BasicAuth = BasicAuth(username, password)
    async with ClientSession(auth=auth) as session:
        yield session


@pytest.fixture(name="client")
async def fixture_client(
    config: dict[str, str],
    session: ClientSession,
) -> AsyncGenerator[CommissionsClient, None]:
    """Yield a CommissionsClient instance."""
    tenant: str = config["SAP_TENANT"]
    yield CommissionsClient(tenant, session, verify_ssl=False)
