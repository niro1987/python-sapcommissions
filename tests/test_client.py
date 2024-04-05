"""Tests for SAP Commissions Client."""
from collections.abc import AsyncGenerator
from typing import TypeVar

import pytest
from sapcommissions import client, const, exceptions, model

T = TypeVar("T", bound="model._Resource")


@pytest.fixture(name="cleanup_resources")
async def fixture_cleanup_resource(
    client: client.CommissionsClient,
) -> AsyncGenerator[list[T]]:
    """Delete created resources from the tenant."""
    created_resources: list[T] = []

    yield created_resources

    for resource in created_resources:
        try:
            await client.delete(resource)
        except exceptions.SAPResponseError:
            const.LOGGER.warning(
                f"Failed to delete resource from tenant: {resource}",
            )

async def test_create_credit_type(
    client: client.CommissionsClient,
    cleanup_resources: list[T],
) -> None:
    """Test create resource."""
    resource = model.CreditType(creditTypeId="TEST")

    created = await client.create(resource)
    assert created.seq is not None
    assert created.creditTypeId == "TEST"

    cleanup_resources.append(created)

async def test_update_credit_type(
    client: client.CommissionsClient,
    cleanup_resources: list[T],
) -> None:
    """Test update resource."""
    resource = model.CreditType(creditTypeId="TEST")

    created = await client.create(resource)
    assert created.seq is not None
    assert created.creditTypeId == "TEST"
    assert created.description is None

    created.description = "UPDATED"
    updated = await client.update(created)
    assert created.seq == updated.seq
    assert updated.creditTypeId == "TEST"
    assert updated.description == "UPDATED"

    cleanup_resources.append(updated)
