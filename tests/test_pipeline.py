"""Tests for running pipelines."""

import logging
from collections.abc import AsyncGenerator
from typing import TypeVar

import pytest

from sapimclient import CommissionsClient, const, helpers, model

LOGGER: logging.Logger = logging.getLogger(__name__)
T = TypeVar("T", bound=model.pipeline._PipelineRunJob)  # pylint: disable=protected-access


pytest.skip("These tests will run pipelines on your tenant", allow_module_level=True)


@pytest.fixture(name="cleanup", scope="session")
async def fixture_delete_pipeline(
    client: CommissionsClient,
) -> AsyncGenerator[list[model.Pipeline], None]:
    """Fixture to delete the created pipeline."""

    pipelines: list[model.Pipeline] = []
    yield pipelines

    for pipeline in pipelines:
        reloaded = await client.read(pipeline)
        if reloaded.state == const.PipelineState.Done:
            LOGGER.info("Pipeline state done: %s", pipeline.pipeline_run_seq)
            continue
        try:
            await client.cancel_pipeline(pipeline)
            LOGGER.info("Pipeline cancelled: %s", pipeline.pipeline_run_seq)
        except Exception:  # pylint: disable=broad-except
            LOGGER.exception("Error deleting pipeline")


@pytest.fixture(name="calendar", scope="session")
async def fixture_calendar(client: CommissionsClient) -> model.Calendar:
    """Fixture to return first calendar instance."""
    if not (calendar := await client.read_first(model.Calendar)):
        pytest.skip("No calendar returned from client.")
    assert calendar.seq is not None, "calendar.seq invalid."

    LOGGER.debug("Calendar %s: %s", calendar.seq, calendar.name)
    return calendar


@pytest.fixture(name="period", scope="session")
async def fixture_period(
    client: CommissionsClient,
    calendar: model.Calendar,
) -> model.Period:
    """Fixture to return first calendar period instance."""
    if not (
        period := await client.read_first(
            model.Period,
            filters=helpers.And(
                helpers.Equals("calendar", str(calendar.seq)),
                helpers.Equals("periodType", str(calendar.minor_period_type)),
            ),
        ),
    ):
        pytest.skip("No period returned from client.")
    assert period.seq, "period.seq invalid."

    LOGGER.debug("Period %s: %s", period.seq, period.name)
    return period


@pytest.mark.parametrize(
    "pipeline_job",
    [
        model.Classify,
        model.Allocate,
        model.Reward,
        model.Pay,
        model.Summarize,
        model.Compensate,
        model.CompensateAndPay,
        model.ResetFromClassify,
        model.ResetFromAllocate,
        model.ResetFromReward,
        model.ResetFromPay,
        model.Post,
        model.Finalize,
        model.UndoPost,
        model.UndoFinalize,
        model.CleanupDefferedResults,
        model.UpdateAnalytics,
    ],
)
async def test_pipelinerun(
    client: CommissionsClient,
    pipeline_job: type[T],
    cleanup: list[model.Pipeline],
    period: model.Period,
) -> None:
    """Test running a pipeline on a calendar period."""

    job: T = pipeline_job(  # type: ignore[call-arg]
        calendar_seq=str(period.calendar),
        period_seq=period.period_seq,
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.pipeline_run_seq is not None
    cleanup.append(result)
    assert result.command == job.command
    assert result.stage_type == job.stage_type_seq
    assert str(result.period) == period.seq


async def test_xmlimport(
    client: CommissionsClient,
    cleanup: list[model.Pipeline],
) -> None:
    """Test running an XML import."""
    job = model.XMLImport(
        xml_file_name="test.xml",
        xml_file_content="<xml></xml>",
        update_existing_objects=True,
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.pipeline_run_seq is not None
    cleanup.append(result)
    assert result.command == job.command
    assert result.stage_type == job.stage_type_seq


@pytest.mark.parametrize(
    "pipeline_job",
    [
        model.Validate,
        model.Transfer,
        model.ValidateAndTransfer,
        model.ValidateAndTransferIfAllValid,
        model.TransferIfAllValid,
    ],
)
async def test_import(
    client: CommissionsClient,
    pipeline_job: type[model.pipeline._ImportJob],
    cleanup: list[model.Pipeline],
    calendar: model.Calendar,
) -> None:
    """Test running an import job."""
    batch_name: str = "test.txt"
    job: model.pipeline._ImportJob = pipeline_job(  # type: ignore[call-arg]
        calendar_seq=calendar.seq,
        batch_name=batch_name,
        module=const.StageTables.TransactionalData,
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.pipeline_run_seq is not None
    cleanup.append(result)
    assert result.stage_type == job.stage_type_seq
    assert result.command == job.command
    assert result.batch_name == job.batch_name


async def test_purge(
    client: CommissionsClient,
    cleanup: list[model.Pipeline],
) -> None:
    """Test running a Purge pipeline."""
    batch_name: str = "test.txt"
    job = model.Purge(
        batch_name=batch_name,
        module=const.StageTables.TransactionalData,
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.pipeline_run_seq is not None
    cleanup.append(result)
    assert result.stage_type == job.stage_type_seq
    assert result.command == job.command
    assert result.batch_name == job.batch_name


async def test_resetfromvalidate(
    client: CommissionsClient,
    cleanup: list[model.Pipeline],
    period: model.Period,
) -> None:
    """Test running a ResetFromValidate pipeline."""
    batch_name: str = "test.txt"
    job: model.ResetFromValidate = model.ResetFromValidate(
        calendar_seq=str(period.calendar),
        period_seq=period.seq,
        batch_name=batch_name,
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.pipeline_run_seq is not None
    cleanup.append(result)
    assert result.stage_type == const.ImportStages.ResetFromValidate
    assert result.command == "Import"
    assert result.batch_name == job.batch_name


async def test_resetfromvalidate_no_batch(
    client: CommissionsClient,
    cleanup: list[model.Pipeline],
    period: model.Period,
) -> None:
    """Test running a ResetFromValidate pipeline without batch_name."""
    job: model.ResetFromValidate = model.ResetFromValidate(
        calendar_seq=str(period.calendar),
        period_seq=period.seq,
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.pipeline_run_seq is not None
    cleanup.append(result)
    assert result.stage_type == const.ImportStages.ResetFromValidate
    assert result.command == "Import"
    assert result.batch_name is None
