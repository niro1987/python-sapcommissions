"""Test for SAP Incentive Management Client."""

from aioresponses import aioresponses

from sapimclient import Tenant
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
