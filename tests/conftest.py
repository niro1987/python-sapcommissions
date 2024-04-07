"""Config for Pytest."""

# pylint: disable=protected-access

import os
from collections.abc import AsyncGenerator, Generator
from inspect import isclass

import pytest
from aiohttp import BasicAuth, ClientSession
from dotenv import load_dotenv

from sapcommissions import CommissionsClient, model


class AsyncLimitedGenerator:
    """Async generator to limit the number of yielded items."""

    def __init__(self, iterable, limit: int):
        """Initialize the async iterator."""
        self.iterable = iterable
        self.limit = limit

    def __aiter__(self):
        """Return the async iterator."""
        return self

    async def __anext__(self):
        """Return the next item in the async iterator."""
        if self.limit == 0:
            raise StopAsyncIteration
        self.limit -= 1
        return await self.iterable.__anext__()


def list_endpoint_cls() -> Generator[type[model._Endpoint], None, None]:
    """List all endpoint classes in the model module."""
    for name in dir(model):
        obj = getattr(model, name)
        if (
            isclass(obj)
            and issubclass(obj, model._Endpoint)
            and not obj.__name__.startswith("_")
        ):
            yield obj


def list_resource_cls() -> Generator[type[model._Resource], None, None]:
    """List all resource classes in the model module."""
    for name in dir(model):
        obj = getattr(model, name)
        if (
            isclass(obj)
            and issubclass(obj, model._Resource)
            and not obj.__name__.startswith("_")
        ):
            yield obj


def list_pipeline_job_cls() -> Generator[type[model._PipelineJob], None, None]:
    """List all pipeline job classes in the model module."""
    for name in dir(model):
        obj = getattr(model, name)
        if (
            isclass(obj)
            and issubclass(obj, model._PipelineJob)
            and not obj.__name__.startswith("_")
        ):
            yield obj


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
