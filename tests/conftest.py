"""Config for Pytest."""

import os
from collections.abc import AsyncGenerator

import pytest
from aiohttp import BasicAuth, ClientSession
from dotenv import load_dotenv

from sapcommissions import CommissionsClient


@pytest.fixture(name="session")
async def fixture_session() -> AsyncGenerator[ClientSession, None]:
    """Yield an async client session."""
    load_dotenv("tests/.env")
    username: str | None = os.environ.get("SAP_USERNAME")
    password: str | None = os.environ.get("SAP_PASSWORD")
    if not (username and password):
        raise ValueError(
            "SAP_USERNAME and SAP_PASSWORD must be set in the environment."
        )
    auth: BasicAuth = BasicAuth(username, password)
    async with ClientSession(auth=auth) as session:
        yield session


@pytest.fixture(name="client")
async def fixture_client(
    session: ClientSession,
) -> AsyncGenerator[CommissionsClient, None]:
    """Yield a CommissionsClient instance."""
    if not (tenant := os.environ.get("SAP_TENANT")):
        raise ValueError("SAP_TENANT must be set in the environment.")
    yield CommissionsClient(tenant, session, verify_ssl=False)
