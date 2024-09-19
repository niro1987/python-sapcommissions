"""Export module for Python SAP Commissions Client."""

import asyncio
from collections.abc import AsyncGenerator, Coroutine
from typing import Any, TypeVar

import pandas as pd

from sapcommissions import CommissionsClient, model
from sapcommissions.exceptions import SAPConnectionError
from sapcommissions.helpers import BooleanOperator, LogicalOperator, retry

GLOB_SEMAPHORE = asyncio.Semaphore(5)
MAX_BUFFER: int = 1000
T = TypeVar("T", bound="model.base.Resource")


async def limited_gather(coro: Coroutine[Any, Any, Any]) -> Any:
    """Limit concurrency."""
    async with GLOB_SEMAPHORE:
        return await coro


def transform_values(series: pd.Series) -> pd.Series:
    """Extract Value object in series."""
    if all(x is None or (isinstance(x, dict) and "value" in x) for x in series):
        return series.apply(lambda x: x["value"] if x else None).astype(float)
    return series


def extract_display_name(series: pd.Series) -> pd.Series:
    """Extract display_name series."""
    if all(x is None or (isinstance(x, dict) and "display_name" in x) for x in series):
        return series.apply(lambda x: x["display_name"] if x else None).astype(str)
    return series


async def load_data(generator: AsyncGenerator[T, None]) -> pd.DataFrame:
    """Load resources to DataFrame."""
    df: pd.DataFrame = pd.DataFrame()
    buffer: list[dict[str, Any]] = []

    async for item in generator:
        buffer.append(item.model_dump())

        if len(buffer) == MAX_BUFFER:
            chunk: pd.DataFrame = pd.DataFrame(buffer, dtype="object")
            df = pd.concat([df, chunk], ignore_index=True)
            buffer.clear()

    if buffer:
        chunk = pd.DataFrame(buffer, dtype="object")
        df = pd.concat([df, chunk], ignore_index=True)

    return df


async def load_ref(
    client: CommissionsClient,
    resource_cls: type[T],
    seqs: list[str],
) -> pd.DataFrame:
    """Load reference resources into DataFrame."""
    df: pd.DataFrame = pd.DataFrame()

    for i in range(0, len(seqs), MAX_BUFFER):
        chunk_seqs: list[str] = seqs[i : i + MAX_BUFFER]
        tasks = [
            limited_gather(
                retry(
                    client.read_seq,
                    resource_cls,
                    seq,
                    exceptions=SAPConnectionError,
                )
            )
            for seq in chunk_seqs
        ]
        result: list[T] = await asyncio.gather(*tasks)
        chunk = pd.DataFrame([item.model_dump() for item in result], dtype="object")
        chunk.set_index(resource_cls.attr_seq, inplace=True)

        df = pd.concat([df, chunk])

    return df


async def load_credits(
    client: CommissionsClient,
    filters: BooleanOperator | LogicalOperator | str | None = None,
) -> pd.DataFrame:
    """Load Credit results extended with reference data to DataFrame."""

    df_credits: pd.DataFrame = await load_data(
        generator=client.read_all(
            resource_cls=model.Credit,
            filters=filters,
            page_size=100,
        )
    )
    df_credits.set_index(model.Credit.attr_seq, inplace=True)
    df_participants: pd.DataFrame = await load_ref(
        client=client,
        resource_cls=model.Participant,
        seqs=(
            df_credits["payee"].apply(lambda x: x["key"]).drop_duplicates().to_list()
        ),
    )
    df_positions: pd.DataFrame = await load_ref(
        client=client,
        resource_cls=model.Position,
        seqs=(
            df_credits["position"].apply(lambda x: x["key"]).drop_duplicates().to_list()
        ),
    )
    df_periods: pd.DataFrame = await load_ref(
        client=client,
        resource_cls=model.Period,
        seqs=df_credits["period"].apply(lambda x: x["key"]).drop_duplicates().to_list(),
    )
    df_event_types: pd.DataFrame = await load_ref(
        client=client,
        resource_cls=model.EventType,
        seqs=(
            df_credits["sales_transaction"]
            .apply(lambda x: x["logical_keys"]["eventType"])
            .drop_duplicates()
            .to_list()
        ),
    )

    df_credits["payee"] = df_credits["payee"].apply(lambda x: x["key"])
    df_credits["position"] = df_credits["position"].apply(lambda x: x["key"])
    df_credits["period"] = df_credits["period"].apply(lambda x: x["key"])
    df_credits["event_type"] = df_credits["sales_transaction"].apply(
        lambda x: x["logical_keys"]["eventType"]
    )

    df: pd.DataFrame = (
        df_credits.join(df_participants[["last_name"]].add_prefix("payee."), on="payee")
        .join(df_positions.add_prefix("position."), on="position")
        .join(df_periods.add_prefix("period."), on="period")
        .join(df_event_types.add_prefix("event_type."), on="event_type")
        .apply(transform_values)
    )
    del df_credits, df_participants, df_positions, df_periods, df_event_types

    df["sales_order.key"] = df["sales_order"].apply(lambda x: x["key"])
    df["sales_order.name"] = df["sales_order"].apply(lambda x: x["display_name"])
    df.drop("sales_order", axis=1, inplace=True)

    df["sales_transaction.key"] = df["sales_transaction"].apply(lambda x: x["key"])
    df["sales_transaction.line_number"] = df["sales_transaction"].apply(
        lambda x: x["logical_keys"]["lineNumber"]["value"]
    )
    df["sales_transaction.sub_line_number"] = df["sales_transaction"].apply(
        lambda x: x["logical_keys"]["subLineNumber"]["value"]
    )

    df.to_csv("test.csv")
    df.dtypes.to_csv("dtypes.csv")

    df["credit_type.name"] = df["credit_type"].apply(lambda x: x["display_name"])
    df["rule.name"] = df["rule"].apply(
        lambda x: x["display_name"] if not pd.isna(x) else None
    )
    df["position.title.name"] = df["position.title"].apply(lambda x: x["display_name"])
    df["period.calendar.name"] = df["period.calendar"].apply(
        lambda x: x["display_name"]
    )
    df["business_units.name"] = df["business_units"].apply(
        lambda x: ", ".join([business_unit["name"] for business_unit in x])
    )
    df["sales_transaction.name"] = (
        df["sales_order.name"]
        + ", Line:"
        + df["sales_transaction.line_number"].astype(str)
        + ", Subline:"
        + df["sales_transaction.sub_line_number"].astype(str)
        + " "
        + df["event_type.event_type_id"]
    )
