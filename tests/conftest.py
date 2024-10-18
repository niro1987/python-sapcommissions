"""Config for Pytest."""

# pylint: disable=protected-access

import os
from collections.abc import AsyncGenerator, Generator, Iterable
from inspect import isclass
from typing import Any

import pytest
from aiohttp import BasicAuth, ClientSession
from aioresponses import aioresponses
from dotenv import load_dotenv
from pytest_asyncio import is_async_test

from sapimclient import Tenant, model


def pytest_collection_modifyitems(items: Iterable[Any]) -> None:
    """Add the session scope marker to async tests."""
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope='session')
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


def list_endpoint_cls() -> Generator[type[model.base.Endpoint], None, None]:
    """List all endpoint classes in the model module."""
    for name in dir(model):
        obj = getattr(model, name)
        if (
            isclass(obj)
            and issubclass(obj, model.base.Endpoint)
            and not obj.__name__.startswith('_')
        ):
            yield obj


def list_pipeline_job_cls() -> Generator[type[model.pipeline._PipelineJob], None, None]:
    """List all pipeline job classes in the model module."""
    for name in dir(model):
        obj = getattr(model, name)
        if (
            isclass(obj)
            and issubclass(obj, model.pipeline._PipelineJob)
            and not obj.__name__.startswith('_')
        ):
            yield obj


def list_resource_cls() -> Generator[type[model.base.Resource], None, None]:
    """List all resource classes in the model module."""
    for name in dir(model):
        obj = getattr(model, name)
        if (
            isclass(obj)
            and issubclass(obj, model.base.Resource)
            and not obj.__name__.startswith('_')
        ):
            yield obj


@pytest.fixture(name='live_session', scope='session')
async def fixture_live_session() -> AsyncGenerator[ClientSession, None]:
    """Yield an authenticated clientsession."""
    load_dotenv('tests/.env')
    username: str | None = os.environ.get('SAP_USERNAME')
    password: str | None = os.environ.get('SAP_PASSWORD')
    if not (username and password):
        pytest.skip('SAP_USERNAME and SAP_PASSWORD must be set in the environment.')
    auth: BasicAuth = BasicAuth(username, password)
    async with ClientSession(auth=auth) as session:
        yield session


@pytest.fixture(name='live_tenant', scope='session')
async def fixture_live_tenant(
    live_session: ClientSession,
) -> Tenant:
    """Yield a Tenant instance."""
    if not (tenant := os.environ.get('SAP_TENANT')):
        pytest.skip('SAP_TENANT must be set in the environment.')
    return Tenant(tenant, live_session, verify_ssl=False)


@pytest.fixture(name='session', scope='session')
async def fixture_session() -> AsyncGenerator[ClientSession, None]:
    """Yield an authenticated clientsession."""
    async with ClientSession() as session:
        yield session


@pytest.fixture(name='tenant', scope='session')
async def fixture_tenant(
    session: ClientSession,
) -> Tenant:
    """Yield a Tenant instance."""
    return Tenant('TEST', session, verify_ssl=False)


@pytest.fixture(name='mocked')
def fixture_mocked_responses() -> Generator[aioresponses, None, None]:
    """Return aioresponses fixture."""
    with aioresponses() as mocker:
        yield mocker
