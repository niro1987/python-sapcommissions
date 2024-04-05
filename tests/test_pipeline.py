"""Tests for running pipelines."""
import logging
from pathlib import Path

import pytest
from sapcommissions import CommissionsClient, const, helpers, model

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize("pipeline_job", [
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
])
async def test_pipelinerun(
    client: CommissionsClient,
    pipeline_job: model._PipelineRunJob,
) -> None:
    """Test running a pipeline on a calendar period."""
    period: model.Period = await client.read(
        model.Period,
        filter=helpers.Equals("name", "202401 W1"),
    )
    job: model._PipelineRunJob = pipeline_job(
        calendarSeq=period.calendar,
        periodSeq=period.periodSeq,
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.command == job.command
    assert result.stageType == job.stageTypeSeq
    assert result.period == period.periodSeq


async def test_pipelinerun_report(
    client: CommissionsClient,
) -> None:
    """Test running a pipeline on a calendar period."""
    period: model.Period = await client.read(
        model.Period,
        filter=helpers.Equals("name", "202401 W1"),
    )
    job: model.ReportsGeneration = model.ReportsGeneration(
        calendarSeq=period.calendar,
        periodSeq=period.periodSeq,
        reportTypeName=const.ReportType.Crystal,
        reportFormatsList=[const.ReportFormat.Excel],
        odsReportList=["Outbound Files"],
        boGroupsList=["VFNL Compensation Reports Admin Group"]
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.command == job.command
    assert result.stageType == job.stageTypeSeq
    assert result.period == period.periodSeq


async def test_xmlimport(
    client: CommissionsClient,
) -> None:
    """Test running an XML import."""
    file: Path = Path("tests/deploy/07_CR_TEST.xml")
    assert file.is_file()

    job = model.XMLImport(
        xmlFileName=file.name,
        xmlFileContent=file.read_text("UTF-8"),
        updateExistingObjects=True,
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.command == job.command
    assert result.stageType == job.stageTypeSeq


@pytest.mark.parametrize("pipeline_job", [
    model.Validate,
    model.Transfer,
    model.ValidateAndTransfer,
    model.ValidateAndTransferIfAllValid,
    model.TransferIfAllValid,
])
async def test_import(
    client: CommissionsClient,
    pipeline_job: model._ImportJob,
) -> None:
    """Test running an import job."""
    batch_name: str = "test.txt"
    calendar: model.Calendar = await client.read(
        model.Calendar,
        filter=helpers.Equals("name", "Main Weekly Calendar"),
    )
    job: model._ImportJob = pipeline_job(
        calendarSeq=calendar.calendarSeq,
        batchName=batch_name,
        module=const.StageTables.TransactionalData,
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.stageType == job.stageTypeSeq
    assert result.command == job.command
    assert result.batchName == job.batchName


async def test_purge(
    client: CommissionsClient,
) -> None:
    """Test running a Purge pipeline."""
    batch_name: str = "test.txt"
    job = model.Purge(
        batchName=batch_name,
        module=const.StageTables.TransactionalData,
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.stageType == job.stageTypeSeq
    assert result.command == job.command
    assert result.batchName == job.batchName


async def test_resetfromvalidate(
    client: CommissionsClient,
) -> None:
    """Test running a ResetFromValidate pipeline."""
    batch_name: str = "test.txt"
    period: model.Period = await client.read(
        model.Period,
        filter=helpers.Equals("name", "202001 W1"),
    )
    job: model.ResetFromValidate = model.ResetFromValidate(
        calendarSeq=period.calendar,
        periodSeq=period.periodSeq,
        batchName=batch_name,
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.stageType == const.ImportStages.ResetFromValidate
    assert result.command == "Import"
    assert result.batchName == job.batchName


async def test_resetfromvalidate_no_batch(
    client: CommissionsClient,
) -> None:
    """Test running a ResetFromValidate pipeline without batchName."""
    period: model.Period = await client.read(
        model.Period,
        filter=helpers.Equals("name", "202001 W1"),
    )
    job: model.ResetFromValidate = model.ResetFromValidate(
        calendarSeq=period.calendar,
        periodSeq=period.periodSeq,
    )
    result: model.Pipeline = await client.run_pipeline(job)
    LOGGER.info(result)
    assert result.stageType == const.ImportStages.ResetFromValidate
    assert result.command == "Import"
    assert result.batchName is None
