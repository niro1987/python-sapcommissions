"""Config for Pytest."""
from collections.abc import AsyncGenerator

import pytest
from aiohttp import BasicAuth, ClientSession
from dotenv import dotenv_values
from sapcommissions import CommissionsClient


@pytest.fixture(name="client")
async def fixture_client() -> AsyncGenerator[CommissionsClient, None]:
    tenant: str = "VFNL-MDEV"
    username, password = dotenv_values("tests/.env").values()
    auth: BasicAuth = BasicAuth(username, password)
    async with ClientSession(auth=auth) as session:
        yield CommissionsClient(tenant, session, verify_ssl=False)

@pytest.fixture(name="client_dev")
async def fixture_client_dev() -> AsyncGenerator[CommissionsClient, None]:
    tenant: str = "VFNL-MDEV"
    username, password = dotenv_values("tests/.env").values()
    auth: BasicAuth = BasicAuth(username, password)
    async with ClientSession(auth=auth) as session:
        yield CommissionsClient(tenant, session, verify_ssl=False)

@pytest.fixture(name="client_tst")
async def fixture_client_tst() -> AsyncGenerator[CommissionsClient, None]:
    tenant: str = "VFNL-MTST"
    username, password = dotenv_values("tests/.env").values()
    auth: BasicAuth = BasicAuth(username, password)
    async with ClientSession(auth=auth) as session:
        yield CommissionsClient(tenant, session, verify_ssl=False)

@pytest.fixture(name="client_uat")
async def fixture_client_uat() -> AsyncGenerator[CommissionsClient, None]:
    tenant: str = "VFNL-MUAT"
    username, password = dotenv_values("tests/.env").values()
    auth: BasicAuth = BasicAuth(username, password)
    async with ClientSession(auth=auth) as session:
        yield CommissionsClient(tenant, session, verify_ssl=False)

@pytest.fixture(name="client_prd")
async def fixture_client_prd() -> AsyncGenerator[CommissionsClient, None]:
    tenant: str = "VFNL-MPRD"
    username, password = dotenv_values("tests/.env").values()
    auth: BasicAuth = BasicAuth(username, password)
    async with ClientSession(auth=auth) as session:
        yield CommissionsClient(tenant, session, verify_ssl=False)
