"""Config for Pytest."""

# pylint: disable=protected-access

import os
from collections.abc import AsyncGenerator, Generator
from inspect import isclass

import pytest
from aiohttp import BasicAuth, ClientSession
from aioresponses import aioresponses
from dotenv import load_dotenv
from pytest_asyncio import is_async_test

from sapcommissions import CommissionsClient, model


def pytest_collection_modifyitems(items):
    """Add the session scope marker to async tests."""
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


def list_resource_cls() -> Generator[type[model.base.Resource], None, None]:
    """List all resource classes in the model module."""
    for name in dir(model):
        obj = getattr(model, name)
        if (
            isclass(obj)
            and issubclass(obj, model.base.Resource)
            and not obj.__name__.startswith("_")
        ):
            yield obj


@pytest.fixture(name="session", scope="session")
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


@pytest.fixture(name="client", scope="session")
async def fixture_client(
    session: ClientSession,
) -> CommissionsClient:
    """Yield a CommissionsClient instance."""
    if not (tenant := os.environ.get("SAP_TENANT")):
        raise ValueError("SAP_TENANT must be set in the environment.")
    return CommissionsClient(tenant, session, verify_ssl=False)


@pytest.fixture(name="responses")
def fixture_responses() -> Generator[aioresponses, None, None]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses
