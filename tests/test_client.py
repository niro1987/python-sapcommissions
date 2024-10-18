"""Test for SAP Incentive Management Client."""

import pytest
from aiohttp import ClientError
from aioresponses import aioresponses

from sapimclient import Tenant, exceptions
from sapimclient.const import HTTPMethod


async def test_tenant_request(
    tenant: Tenant,
    mocked: aioresponses,
) -> None:
    """Test tenant request happy flow."""
    mocked.get(
        url=f'{tenant.host}/spamm',
        status=200,
        headers={'Content-Type': 'application/json'},
        payload={'eggs': 'bacon'},
    )

    response = await tenant._request(method=HTTPMethod.GET, uri='spamm')
    assert response == {'eggs': 'bacon'}


async def test_tenant_request_timeout(
    tenant: Tenant,
    mocked: aioresponses,
) -> None:
    """Test tenant request exceed timeout."""
    mocked.get(
        url=f'{tenant.host}/spamm',
        exception=TimeoutError(),
    )
    with pytest.raises(exceptions.SAPConnectionError):
        await tenant._request(method=HTTPMethod.GET, uri='spamm')

    mocked.get(
        url=f'{tenant.host}/eggs',
        timeout=True,
    )
    with pytest.raises(exceptions.SAPConnectionError):
        await tenant._request(method=HTTPMethod.GET, uri='eggs')


async def test_tenant_request_no_connection(
    tenant: Tenant,
    mocked: aioresponses,
) -> None:
    """Test tenant request ClientError."""
    mocked.get(
        url=f'{tenant.host}/spamm',
        exception=ClientError(),
    )
    with pytest.raises(exceptions.SAPConnectionError):
        await tenant._request(method=HTTPMethod.GET, uri='spamm')


async def test_tenant_request_not_modified(
    tenant: Tenant,
    mocked: aioresponses,
) -> None:
    """Test tenant request happy flow."""
    mocked.post(
        url=f'{tenant.host}/spamm',
        status=304,
    )

    with pytest.raises(exceptions.SAPNotModifiedError):
        await tenant._request(
            method=HTTPMethod.POST,
            uri='spamm',
            json=[{'eggs': 'bacon'}],
        )


async def test_tenant_request_maintenance(
    tenant: Tenant,
    mocked: aioresponses,
) -> None:
    """Test tenant request happy flow."""
    mocked.get(
        url=f'{tenant.host}/spamm',
        status=200,
        headers={'Content-Type': 'text/html'},
        payload='<html><body>Server Maintenance</body></html>',
    )

    with pytest.raises(exceptions.SAPResponseError):
        await tenant._request(method=HTTPMethod.GET, uri='spamm')


async def test_tenant_request_status(
    tenant: Tenant,
    mocked: aioresponses,
) -> None:
    """Test tenant request status code."""
    mocked.get(
        url=f'{tenant.host}/200',
        status=200,
        headers={'Content-Type': 'application/json'},
        payload={'eggs': 'bacon'},
    )
    response = await tenant._request(method=HTTPMethod.GET, uri='200')
    assert response.get('eggs') == 'bacon'

    mocked.get(
        url=f'{tenant.host}/300',
        status=300,
        headers={'Content-Type': 'application/json'},
        payload={'eggs': 'bacon'},
    )
    with pytest.raises(exceptions.SAPBadRequestError):
        await tenant._request(method=HTTPMethod.GET, uri='300')

    mocked.post(
        url=f'{tenant.host}/200',
        status=200,
        headers={'Content-Type': 'application/json'},
        payload={'eggs': 'bacon'},
    )
    response = await tenant._request(
        method=HTTPMethod.POST,
        uri='200',
        json=[{'eggs': 'bacon'}],
    )
    assert response.get('eggs') == 'bacon'

    mocked.post(
        url=f'{tenant.host}/201',
        status=201,
        headers={'Content-Type': 'application/json'},
        payload={'eggs': 'bacon'},
    )
    response = await tenant._request(
        method=HTTPMethod.POST,
        uri='201',
        json=[{'eggs': 'bacon'}],
    )
    assert response.get('eggs') == 'bacon'

    mocked.post(
        url=f'{tenant.host}/300',
        status=300,
        headers={'Content-Type': 'application/json'},
        payload={'eggs': 'bacon'},
    )
    with pytest.raises(exceptions.SAPBadRequestError):
        await tenant._request(
            method=HTTPMethod.POST,
            uri='300',
            json=[{'eggs': 'bacon'}],
        )

    mocked.put(
        url=f'{tenant.host}/200',
        status=200,
        headers={'Content-Type': 'application/json'},
        payload={'eggs': 'bacon'},
    )
    response = await tenant._request(method=HTTPMethod.PUT, uri='200')
    assert response.get('eggs') == 'bacon'

    mocked.put(
        url=f'{tenant.host}/300',
        status=300,
        headers={'Content-Type': 'application/json'},
        payload={'eggs': 'bacon'},
    )
    with pytest.raises(exceptions.SAPBadRequestError):
        await tenant._request(method=HTTPMethod.PUT, uri='300')

    mocked.delete(
        url=f'{tenant.host}/200',
        status=200,
        headers={'Content-Type': 'application/json'},
        payload={'eggs': 'bacon'},
    )
    response = await tenant._request(method=HTTPMethod.DELETE, uri='200')
    assert response.get('eggs') == 'bacon'

    mocked.delete(
        url=f'{tenant.host}/300',
        status=300,
        headers={'Content-Type': 'application/json'},
        payload={'eggs': 'bacon'},
    )
    with pytest.raises(exceptions.SAPBadRequestError):
        await tenant._request(method=HTTPMethod.DELETE, uri='300')
