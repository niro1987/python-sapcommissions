"""Export module for Python SAP Commissions Client."""

import asyncio
from collections.abc import AsyncGenerator, Coroutine
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

from sapcommissions import CommissionsClient, model
from sapcommissions.exceptions import SAPConnectionError
from sapcommissions.helpers import BooleanOperator, LogicalOperator, retry
from sapcommissions.model.base import Reference, Resource, Value

GLOB_SEMAPHORE = asyncio.Semaphore(5)
MAX_BUFFER: int = 1000


async def limited_gather(coro: Coroutine[Any, Any, Any]) -> Any:
    """Limit concurrency."""
    async with GLOB_SEMAPHORE:
        return await coro


def _transform_dates(series: pd.Series) -> pd.Series:
    """Transform date series to string."""
    return series.apply(lambda x: x.strftime("%m/%d/%Y") if pd.notna(x) else pd.NA)


def _transform_bools(series: pd.Series) -> pd.Series:
    """Transform date series to string."""
    return series.apply(lambda x: int(x) if pd.notna(x) else pd.NA)


def _transform_values(series: pd.Series) -> pd.Series:
    """Extract Value object in series."""
    return series.apply(
        lambda x: x["value"]
        if pd.notna(x) and isinstance(x, dict) and "value" in x
        else pd.NA
    )


def _transform_reference_key(series: pd.Series) -> pd.Series:
    """Extract key from reference series."""
    return series.apply(
        lambda x: x["key"]
        if pd.notna(x) and isinstance(x, dict) and "logical_keys" in x
        else x
    )


def _transform_reference_display_name(series: pd.Series) -> pd.Series:
    """Extract display_name from reference series."""
    return series.apply(
        lambda x: x["display_name"]
        if pd.notna(x) and isinstance(x, dict) and "display_name" in x
        else pd.NA
    )


def _transform_reference_logical_keys(series: pd.Series) -> pd.Series:
    """Extract logical_keys from reference series."""
    return series.apply(
        lambda x: x["logical_keys"]
        if pd.notna(x) and isinstance(x, dict) and "logical_keys" in x
        else pd.NA
    )


def _transform_business_units(series: pd.Series) -> pd.Series:
    """Join business_units to single string."""
    return series.apply(lambda x: ", ".join(str(item) for item in x) if x else pd.NA)


def _transform_all(
    df: pd.DataFrame,
    resource_cls: type[Resource],
) -> pd.DataFrame:
    """Transform and extract all objectes to values."""

    date_fields: list[str] = [
        key for key in resource_cls.typed_fields(date) if key in df.columns
    ]
    df[date_fields] = df[date_fields].apply(_transform_dates)
    bool_fields: list[str] = [
        key for key in resource_cls.typed_fields(bool) if key in df.columns
    ]
    df[bool_fields] = df[bool_fields].apply(_transform_bools)
    value_fields: list[str] = [
        key for key in resource_cls.typed_fields(Value) if key in df.columns
    ]
    df[value_fields] = df[value_fields].apply(_transform_values)
    reference_fields: list[str] = [
        key for key in resource_cls.typed_fields(Reference) if key in df.columns
    ]
    name_fields: list[str] = [f"{field_name}_name" for field_name in reference_fields]
    keys_fields: list[str] = [f"{field_name}_keys" for field_name in reference_fields]
    df[name_fields] = df[reference_fields].apply(_transform_reference_display_name)
    df[keys_fields] = df[reference_fields].apply(_transform_reference_logical_keys)
    df[reference_fields] = df[reference_fields].apply(_transform_reference_key)

    if "business_units" in df.columns:
        df[["business_units"]] = df[["business_units"]].apply(_transform_business_units)

    return df


async def load_resource_filtered(
    client: CommissionsClient,
    resource_cls: type[Resource],
    filters: BooleanOperator | LogicalOperator | str | None = None,
) -> pd.DataFrame:
    """Load resources to DataFrame."""
    generator: AsyncGenerator[Resource, None] = client.read_all(
        resource_cls=resource_cls,
        filters=filters,
        page_size=100,
    )

    df: pd.DataFrame = pd.DataFrame()
    buffer: list[dict[str, Any]] = []

    async for item in generator:
        buffer.append(item.model_dump())

        if len(buffer) == MAX_BUFFER:
            chunk: pd.DataFrame = pd.DataFrame(data=buffer, dtype="object").set_index(
                resource_cls.attr_seq
            )
            df = pd.concat([df, chunk])
            buffer.clear()

    if buffer:
        chunk = pd.DataFrame(buffer, dtype="object").set_index(resource_cls.attr_seq)
        df = pd.concat([df, chunk])

    if df.empty:
        raise ValueError("No results returned.")

    return _transform_all(df, resource_cls)


async def load_resource_seqs(
    client: CommissionsClient,
    resource_cls: type[Resource],
    seqs: set[str] | pd.Series,
) -> pd.DataFrame:
    """Load reference resources into DataFrame."""
    df: pd.DataFrame = pd.DataFrame()
    _seqs: list[str]
    if isinstance(seqs, pd.Series):
        _seqs = seqs.astype(str).drop_duplicates().to_list()
    else:
        _seqs = list(seqs)
    for i in range(0, len(_seqs), MAX_BUFFER):
        chunk_seqs: list[str] = _seqs[i : i + MAX_BUFFER]
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
        result: list[Resource] = await asyncio.gather(*tasks)
        chunk = pd.DataFrame([item.model_dump() for item in result], dtype="object")
        chunk.set_index(resource_cls.attr_seq, inplace=True)

        df = pd.concat([df, chunk])

    return _transform_all(df, resource_cls)


async def load_credits(
    client: CommissionsClient,
    filters: BooleanOperator | LogicalOperator | str | None = None,
    filename: Path | None = None,
) -> pd.DataFrame:
    """Load Credit results extended with reference data to DataFrame."""
    df_credits: pd.DataFrame = await load_resource_filtered(
        client=client,
        resource_cls=model.Credit,
        filters=filters,
    )
    df_credits["order_id"] = df_credits["sales_order_keys"].apply(
        lambda x: x["orderId"] if pd.notna(x) else pd.NA
    )
    df_credits["line_number"] = df_credits["sales_transaction_keys"].apply(
        lambda x: x["lineNumber"] if pd.notna(x) else pd.NA
    )
    df_credits["sub_line_number"] = df_credits["sales_transaction_keys"].apply(
        lambda x: x["subLineNumber"] if pd.notna(x) else pd.NA
    )
    df_credits["event_type"] = df_credits["sales_transaction_keys"].apply(
        lambda x: x["eventType"] if pd.notna(x) else pd.NA
    )

    value_fields: list[str] = ["line_number", "sub_line_number"]
    df_credits[value_fields] = df_credits[value_fields].apply(_transform_values)

    participants: set[str] = {str(item) for item in df_credits["payee"]}
    positions: set[str] = {str(item) for item in df_credits["position"]}
    periods: set[str] = {str(item) for item in df_credits["period"]}
    event_types: set[str] = {str(item) for item in df_credits["event_type"]}

    df_participants: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Participant, seqs=participants
    )
    df_positions: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Position, seqs=positions
    )
    df_periods: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Period, seqs=periods
    )
    df_event_types: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.EventType, seqs=event_types
    )

    df: pd.DataFrame = (
        df_credits.join(df_participants.add_prefix("payee."), on="payee")
        .join(df_positions.add_prefix("position."), on="position")
        .join(df_periods.add_prefix("period."), on="period")
        .join(df_event_types.add_prefix("event_type."), on="event_type")
    )

    df["transaction"] = (
        df["sales_order_name"]
        + ", Line:"
        + df["line_number"].astype(str)
        + ", Subline:"
        + df["sub_line_number"].astype(str)
        + " "
        + df["event_type.event_type_id"]
    )

    if filename:
        columns = {
            "payee.last_name": "Participant",
            "position.name": "Position",
            "position.title_name": "Title",
            "period.name": "Period",
            "name": "Name",
            "value": "Value",
            "pipeline_run_date": "Create Date",
            "rule_name": "Rule",
            "sales_order_name": "Order ID",
            "transaction": "Transaction",
            "credit_type_name": "Credit Type",
            "origin_type_id": "Origin Type",
            "preadjusted_value": "PreAdjusted",
            "is_held": "Ever Held",
            "release_date": "Release Date",
            "compensation_date": "Compensation Date",
            "is_rollable": "Rollable Credit",
            "roll_date": "Roll Date",
            "reason_name": "Reason Code",
            "comments": "Comments",
            "business_units": "Business Unit",
            "ga1": "GA1",
            "ga2": "GA2",
            "ga3": "GA3",
            "ga4": "GA4",
            "ga5": "GA5",
            "ga6": "GA6",
            "ga7": "GA7",
            "ga8": "GA8",
            "ga9": "GA9",
            "ga10": "GA10",
            "ga11": "GA11",
            "ga12": "GA12",
            "ga13": "GA13",
            "ga14": "GA14",
            "ga15": "GA15",
            "ga16": "GA16",
            "gb1": "GB1",
            "gb2": "GB2",
            "gb3": "GB3",
            "gb4": "GB4",
            "gb5": "GB5",
            "gb6": "GB6",
            "gd1": "GD1",
            "gd2": "GD2",
            "gd3": "GD3",
            "gd4": "GD4",
            "gd5": "GD5",
            "gd6": "GD6",
            "gn1": "GN1",
            "gn2": "GN2",
            "gn3": "GN3",
            "gn4": "GN4",
            "gn5": "GN5",
            "gn6": "GN6",
            "period.calendar_name": "Calendar",
        }
        final_df: pd.DataFrame = df[columns.keys()].rename(columns=columns).fillna("")
        final_df.to_csv(filename, index=False)

    return df.fillna("")


async def load_measurements(
    client: CommissionsClient,
    filters: BooleanOperator | LogicalOperator | str | None = None,
    filename: Path | None = None,
) -> pd.DataFrame:
    """Load Credit results extended with reference data to DataFrame."""
    df_measure: pd.DataFrame = await load_resource_filtered(
        client=client,
        resource_cls=model.Measurement,
        filters=filters,
    )

    participants: set[str] = {str(item) for item in df_measure["payee"]}
    positions: set[str] = {str(item) for item in df_measure["position"]}
    periods: set[str] = {str(item) for item in df_measure["period"]}

    df_participants: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Participant, seqs=participants
    )
    df_positions: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Position, seqs=positions
    )
    df_periods: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Period, seqs=periods
    )

    df: pd.DataFrame = (
        df_measure.join(df_participants.add_prefix("payee."), on="payee")
        .join(df_positions.add_prefix("position."), on="position")
        .join(df_periods.add_prefix("period."), on="period")
    )

    if filename:
        columns = {
            "payee.last_name": "Participant",
            "position.name": "Position",
            "position.title_name": "Title",
            "period.name": "Period",
            "name": "Name",
            "value": "Value",
            "pipeline_run_date": "Create Date",
            "rule_name": "Rule",
            "number_of_credits": "Number of Credits",
            "business_units": "Business Unit",
            "ga1": "GA1",
            "ga2": "GA2",
            "ga3": "GA3",
            "ga4": "GA4",
            "ga5": "GA5",
            "ga6": "GA6",
            "ga7": "GA7",
            "ga8": "GA8",
            "ga9": "GA9",
            "ga10": "GA10",
            "ga11": "GA11",
            "ga12": "GA12",
            "ga13": "GA13",
            "ga14": "GA14",
            "ga15": "GA15",
            "ga16": "GA16",
            "gb1": "GB1",
            "gb2": "GB2",
            "gb3": "GB3",
            "gb4": "GB4",
            "gb5": "GB5",
            "gb6": "GB6",
            "gd1": "GD1",
            "gd2": "GD2",
            "gd3": "GD3",
            "gd4": "GD4",
            "gd5": "GD5",
            "gd6": "GD6",
            "gn1": "GN1",
            "gn2": "GN2",
            "gn3": "GN3",
            "gn4": "GN4",
            "gn5": "GN5",
            "gn6": "GN6",
        }
        final_df: pd.DataFrame = df[columns.keys()].rename(columns=columns).fillna("")
        final_df.to_csv(filename, index=False)

    return df.fillna("")


async def load_incentives(
    client: CommissionsClient,
    filters: BooleanOperator | LogicalOperator | str | None = None,
    filename: Path | None = None,
) -> pd.DataFrame:
    """Load Credit results extended with reference data to DataFrame."""
    df_incentive: pd.DataFrame = await load_resource_filtered(
        client=client,
        resource_cls=model.Incentive,
        filters=filters,
    )

    participants: set[str] = {str(item) for item in df_incentive["payee"]}
    positions: set[str] = {str(item) for item in df_incentive["position"]}
    periods: set[str] = {str(item) for item in df_incentive["period"]}

    df_participants: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Participant, seqs=participants
    )
    df_positions: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Position, seqs=positions
    )
    df_periods: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Period, seqs=periods
    )

    df: pd.DataFrame = (
        df_incentive.join(df_participants.add_prefix("payee."), on="payee")
        .join(df_positions.add_prefix("position."), on="position")
        .join(df_periods.add_prefix("period."), on="period")
    )

    if filename:
        columns = {
            "payee.last_name": "Participant",
            "position.name": "Position",
            "position.title_name": "Title",
            "period.name": "Period",
            "name": "Name",
            "value": "Value",
            "pipeline_run_date": "Create Date",
            "rule_name": "Rule",
            "release_date": "Release Date",
            "quota": "Quota",
            "attainment": "Attainment",
            "is_active": "Is Active",
            "business_units": "Business Unit",
            "ga1": "GA1",
            "ga2": "GA2",
            "ga3": "GA3",
            "ga4": "GA4",
            "ga5": "GA5",
            "ga6": "GA6",
            "ga7": "GA7",
            "ga8": "GA8",
            "ga9": "GA9",
            "ga10": "GA10",
            "ga11": "GA11",
            "ga12": "GA12",
            "ga13": "GA13",
            "ga14": "GA14",
            "ga15": "GA15",
            "ga16": "GA16",
            "gb1": "GB1",
            "gb2": "GB2",
            "gb3": "GB3",
            "gb4": "GB4",
            "gb5": "GB5",
            "gb6": "GB6",
            "gd1": "GD1",
            "gd2": "GD2",
            "gd3": "GD3",
            "gd4": "GD4",
            "gd5": "GD5",
            "gd6": "GD6",
            "gn1": "GN1",
            "gn2": "GN2",
            "gn3": "GN3",
            "gn4": "GN4",
            "gn5": "GN5",
            "gn6": "GN6",
        }
        final_df: pd.DataFrame = df[columns.keys()].rename(columns=columns).fillna("")
        final_df.to_csv(filename, index=False)

    return df.fillna("")


async def load_commissions(
    client: CommissionsClient,
    filters: BooleanOperator | LogicalOperator | str | None = None,
    filename: Path | None = None,
) -> pd.DataFrame:
    """Load Credit results extended with reference data to DataFrame."""
    df_commmission: pd.DataFrame = await load_resource_filtered(
        client=client,
        resource_cls=model.Commission,
        filters=filters,
    )

    participants: set[str] = {str(item) for item in df_commmission["payee"]}
    positions: set[str] = {str(item) for item in df_commmission["position"]}
    periods: set[str] = {str(item) for item in df_commmission["period"]}

    df_participants: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Participant, seqs=participants
    )
    df_positions: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Position, seqs=positions
    )
    df_periods: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Period, seqs=periods
    )

    df: pd.DataFrame = (
        df_commmission.join(df_participants.add_prefix("payee."), on="payee")
        .join(df_positions.add_prefix("position."), on="position")
        .join(df_periods.add_prefix("period."), on="period")
    )

    if filename:
        columns = {
            "business_units": "Business Unit",
            "payee.last_name": "Participant",
            "position.name": "Position",
            "position.title_name": "Title",
            "period.name": "Period",
            "entry_number": "Entry Number",
            "name": "Name",
            "rate": "Rate",
            "value": "Value",
            "rule_name": "Rule",
            "pipeline_run_date": "Create Date",
            "credit": "Credit",
            "credit_type": "Credit Type",
            "transaction": "Transaction",
            "incentive": "Incentive",
            "origin_type": "Origin Type",
        }
        final_df: pd.DataFrame = df[columns.keys()].rename(columns=columns).fillna("")
        final_df.to_csv(filename, index=False)

    return df.fillna("")


async def load_deposits(
    client: CommissionsClient,
    filters: BooleanOperator | LogicalOperator | str | None = None,
    filename: Path | None = None,
) -> pd.DataFrame:
    """Load Credit results extended with reference data to DataFrame."""
    df_deposit: pd.DataFrame = await load_resource_filtered(
        client=client,
        resource_cls=model.Deposit,
        filters=filters,
    )

    participants: set[str] = {str(item) for item in df_deposit["payee"]}
    positions: set[str] = {str(item) for item in df_deposit["position"]}
    periods: set[str] = {str(item) for item in df_deposit["period"]}

    df_participants: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Participant, seqs=participants
    )
    df_positions: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Position, seqs=positions
    )
    df_periods: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Period, seqs=periods
    )

    df: pd.DataFrame = (
        df_deposit.join(df_participants.add_prefix("payee."), on="payee")
        .join(df_positions.add_prefix("position."), on="position")
        .join(df_periods.add_prefix("period."), on="period")
    )

    if filename:
        columns = {
            "payee.last_name": "Participant",
            "position.name": "Position",
            "position.title_name": "Title",
            "period.name": "Period",
            "name": "Name",
            "value": "Value",
            "pipeline_run_date": "Create Date",
            "rule_name": "Rule",
            "earning_group_id": "Earning Group",
            "earning_code_id": "Earning Code",
            "origin_type_id": "Origin Type",
            "preadjusted_value": "PreAdjusted",
            "is_held": "Ever Held",
            "release_date": "Release Date",
            "deposit_date": "Deposit Date",
            "reason": "Reason Code",
            "comments": "Comments",
            "business_units": "Business Unit",
            "ga1": "GA1",
            "ga2": "GA2",
            "ga3": "GA3",
            "ga4": "GA4",
            "ga5": "GA5",
            "ga6": "GA6",
            "ga7": "GA7",
            "ga8": "GA8",
            "ga9": "GA9",
            "ga10": "GA10",
            "ga11": "GA11",
            "ga12": "GA12",
            "ga13": "GA13",
            "ga14": "GA14",
            "ga15": "GA15",
            "ga16": "GA16",
            "gb1": "GB1",
            "gb2": "GB2",
            "gb3": "GB3",
            "gb4": "GB4",
            "gb5": "GB5",
            "gb6": "GB6",
            "gd1": "GD1",
            "gd2": "GD2",
            "gd3": "GD3",
            "gd4": "GD4",
            "gd5": "GD5",
            "gd6": "GD6",
            "gn1": "GN1",
            "gn2": "GN2",
            "gn3": "GN3",
            "gn4": "GN4",
            "gn5": "GN5",
            "gn6": "GN6",
            "period.calendar_name": "Calendar",
        }
        final_df: pd.DataFrame = df[columns.keys()].rename(columns=columns).fillna("")
        final_df.to_csv(filename, index=False)

    return df.fillna("")


async def load_payment_summary(
    client: CommissionsClient,
    filters: BooleanOperator | LogicalOperator | str | None = None,
    filename: Path | None = None,
) -> pd.DataFrame:
    """Load Credit results extended with reference data to DataFrame."""
    df_deposit: pd.DataFrame = await load_resource_filtered(
        client=client,
        resource_cls=model.PaymentSummary,
        filters=filters,
    )

    participants: set[str] = {str(item) for item in df_deposit["participant"]}
    positions: set[str] = {str(item) for item in df_deposit["position"]}
    periods: set[str] = {str(item) for item in df_deposit["period"]}

    df_participants: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Participant, seqs=participants
    )
    df_positions: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Position, seqs=positions
    )
    df_periods: pd.DataFrame = await load_resource_seqs(
        client=client, resource_cls=model.Period, seqs=periods
    )

    df: pd.DataFrame = (
        df_deposit.join(df_participants.add_prefix("payee."), on="participant")
        .join(df_positions.add_prefix("position."), on="position")
        .join(df_periods.add_prefix("period."), on="period")
    )

    if filename:
        columns = {
            "payee.last_name": "Participant",
            "position.name": "Position",
            "earning_group_id": "Earning Group",
            "period.name": "Period",
            "prior_balance": "Prior Balance",
            "applied_deposit": "Earning",
            "payment": "Payment",
            "balance": "Balance",
            "business_units": "Business Unit",
        }
        final_df: pd.DataFrame = df[columns.keys()].rename(columns=columns).fillna("")
        final_df.to_csv(filename, index=False)

    return df.fillna("")
