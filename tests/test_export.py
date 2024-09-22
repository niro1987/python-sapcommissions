"""Test the export module."""

import logging
from typing import TypeVar

import pandas as pd
import pytest

from sapcommissions import CommissionsClient, export, helpers, model
from sapcommissions.helpers import AsyncLimitedGenerator
from sapcommissions.model.base import Resource

LOGGER = logging.getLogger(__name__)
T = TypeVar("T", bound=Resource)


@pytest.mark.parametrize(
    "resource_cls",
    [model.Participant, model.Position, model.Period, model.EventType],
)
async def test_load_resource_seqs(
    client: CommissionsClient,
    resource_cls: type[T],
) -> None:
    """Test the load_resource_seqs function."""
    resources: list[T] = []
    generator = client.read_all(resource_cls, page_size=100)
    async for resource in AsyncLimitedGenerator(generator, 1000):
        resources.append(resource)

    seqs: set[str] = {resource.seq for resource in resources if resource.seq}
    df: pd.DataFrame = await export.load_resource_seqs(client, resource_cls, seqs)
    assert isinstance(df, pd.DataFrame)

    df.to_csv(f"tests/export/{resource_cls.__name__}.csv")


async def test_load_credits(client: CommissionsClient) -> None:
    """Test the load_credits function."""
    # client.tenant = "VFNL-MPRD"
    filters: str = " and ".join(
        [
            str(helpers.Equals("period/calendar/name", "Telesales Outbound Calendar")),
            str(helpers.Equals("period/name", "August 2024")),
            str(helpers.Equals("genericNumber1", "302 integer")),
        ]
    )
    df = await export.load_credits(client, filters)
    df.to_csv("tests/export/credits.csv", index=False)


async def test_load_measurements(client: CommissionsClient) -> None:
    """Test the load_measurements function."""
    # client.tenant = "VFNL-MPRD"
    filters: str = " and ".join(
        [
            str(helpers.Equals("period/calendar/name", "Telesales Outbound Calendar")),
            str(helpers.Equals("period/name", "August 2024")),
        ]
    )
    df = await export.load_measurements(client, filters)
    df.to_csv("tests/export/measurements.csv", index=False)


async def test_load_incentives(client: CommissionsClient) -> None:
    """Test the load_incentives function."""
    # client.tenant = "VFNL-MPRD"
    filters: str = " and ".join(
        [
            str(helpers.Equals("period/calendar/name", "Telesales Outbound Calendar")),
            str(helpers.Equals("period/name", "August 2024")),
        ]
    )
    df = await export.load_incentives(client, filters)
    df.to_csv("tests/export/incentives.csv", index=False)


async def test_load_deposits(client: CommissionsClient) -> None:
    """Test the load_deposits function."""
    # client.tenant = "VFNL-MPRD"
    filters: str = " and ".join(
        [
            str(helpers.Equals("period/calendar/name", "Telesales Outbound Calendar")),
            str(helpers.Equals("period/name", "August 2024")),
        ]
    )
    df = await export.load_deposits(client, filters)
    df.to_csv("tests/export/deposits.csv", index=False)


async def test_load_payment_summary(client: CommissionsClient) -> None:
    """Test the load_payment_summary function."""
    # client.tenant = "VFNL-MPRD"
    filters: str = " and ".join(
        [
            str(helpers.Equals("period/calendar/name", "Fiscal Monthly Calendar")),
            str(helpers.Equals("period/name", "*2024")),
        ]
    )
    df = await export.load_payment_summary(client, filters)
    df.to_csv("tests/export/payment_summary.csv", index=False)
