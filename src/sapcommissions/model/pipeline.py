"""Pipeline models for Python SAP Commissions Client."""

from typing import ClassVar, Literal

from pydantic import Field, computed_field, model_validator

from sapcommissions import const

from .base import Endpoint

STAGETABLES: dict[str, list[str]] = {
    "TransactionalData": [
        "TransactionAndCredit",
        "Deposit",
    ],
    "OrganizationData": [
        "Participant",
        "Position",
        "Title",
        "PositionRelation",
    ],
    "ClassificationData": [
        "Category",
        "Category_Classifiers",
        "Customer",
        "Product",
        "PostalCode",
        "GenericClassifier",
    ],
    "PlanRelatedData": [
        "FixedValue",
        "VariableAssignment",
        "Quota",
        "RelationalMDLT",
    ],
}


class _PipelineJob(Endpoint):
    """Base class for a Pipeline Job."""

    attr_endpoint: ClassVar[str] = "api/v2/pipelines"
    command: Literal["PipelineRun", "Import", "XMLImport"]
    run_stats: bool = False


class ResetFromValidate(_PipelineJob):
    """Run a ResetFromValidate pipeline."""

    attr_endpoint: ClassVar[str] = "api/v2/pipelines/resetfromvalidate"
    command: Literal["Import"] = "Import"
    calendar_seq: str
    period_seq: str
    batch_name: str | None = None


class Purge(_PipelineJob):
    """Run a Purge pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.Purge] = (
        const.PipelineRunStages.Purge
    )
    command: Literal["PipelineRun"] = "PipelineRun"
    batch_name: str
    module: const.StageTables

    @computed_field
    def stage_tables(self) -> list[str]:
        """Compute stageTables field based on module."""
        return STAGETABLES[self.module]


class XMLImport(_PipelineJob):
    """Run an XML Import pipeline."""

    command: Literal["XMLImport"] = "XMLImport"
    stage_type_seq: Literal[const.XMLImportStages.XMLImport] = (
        const.XMLImportStages.XMLImport
    )
    xml_file_name: str
    xml_file_content: str
    update_existing_objects: bool = False


class _PipelineRunJob(_PipelineJob):
    """Base class for a PipelineRun job."""

    command: Literal["PipelineRun"] = "PipelineRun"
    period_seq: str
    calendar_seq: str
    stage_type_seq: const.PipelineRunStages
    run_mode: const.PipelineRunMode = const.PipelineRunMode.Full
    position_groups: list[str] | None = None
    position_seqs: list[str] | None = None
    processing_unit_seq: str | None = None

    @model_validator(mode="after")
    def check_runmode(self) -> "_PipelineRunJob":
        """Validate run_mode together with position_groups and position_seqs."""
        if self.run_mode in (
            const.PipelineRunMode.Full,
            const.PipelineRunMode.Incremental,
        ) and not (self.position_groups is None and self.position_seqs is None):
            raise ValueError(
                "When run_mode is 'full' or 'incremental' "
                "position_groups and position_seqs must be None"
            )
        if self.run_mode == const.PipelineRunMode.Positions and not (
            self.position_groups or self.position_seqs
        ):
            raise ValueError(
                "When run_mode is 'positions' "
                "provide either position_groups or position_seqs"
            )

        if self.position_groups and self.position_seqs:
            raise ValueError(
                "Provide either position_groups or position_seqs, not both"
            )

        return self


class Classify(_PipelineRunJob):
    """Run a Classify pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.Classify] = (
        const.PipelineRunStages.Classify
    )
    run_mode: Literal[const.PipelineRunMode.Full, const.PipelineRunMode.Incremental] = (
        const.PipelineRunMode.Full
    )
    position_groups: None = None
    position_seqs: None = None


class Allocate(_PipelineRunJob):
    """Run an Allocate pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.Allocate] = (
        const.PipelineRunStages.Allocate
    )


class Reward(_PipelineRunJob):
    """Run a Reward pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.Reward] = (
        const.PipelineRunStages.Reward
    )
    run_mode: Literal[const.PipelineRunMode.Full, const.PipelineRunMode.Positions] = (
        const.PipelineRunMode.Full
    )


class Pay(_PipelineRunJob):
    """Run a Pay pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.Pay] = const.PipelineRunStages.Pay
    run_mode: Literal[const.PipelineRunMode.Full, const.PipelineRunMode.Positions] = (
        const.PipelineRunMode.Full
    )
    position_seqs: None = None


class Summarize(_PipelineRunJob):
    """Run a Summarize pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.Summarize] = (
        const.PipelineRunStages.Summarize
    )


class Compensate(_PipelineRunJob):
    """Run a Compensate pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.Compensate] = (
        const.PipelineRunStages.Compensate
    )
    remove_stale_results: bool = False


class CompensateAndPay(_PipelineRunJob):
    """Run a CompensateAndPay pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.CompensateAndPay] = (
        const.PipelineRunStages.CompensateAndPay
    )
    remove_stale_results: bool = False


class ResetFromClassify(_PipelineRunJob):
    """Run a ResetFromClassify pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.ResetFromClassify] = (
        const.PipelineRunStages.ResetFromClassify
    )


class ResetFromAllocate(_PipelineRunJob):
    """Run a ResetFromAllocate pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.ResetFromAllocate] = (
        const.PipelineRunStages.ResetFromAllocate
    )


class ResetFromReward(_PipelineRunJob):
    """Run a ResetFromReward pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.ResetFromReward] = (
        const.PipelineRunStages.ResetFromReward
    )


class ResetFromPay(_PipelineRunJob):
    """Run a ResetFromPay pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.ResetFromPay] = (
        const.PipelineRunStages.ResetFromPay
    )


class Post(_PipelineRunJob):
    """Run a Post pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.Post] = const.PipelineRunStages.Post


class Finalize(_PipelineRunJob):
    """Run a Finalize pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.Finalize] = (
        const.PipelineRunStages.Finalize
    )


class ReportsGeneration(_PipelineRunJob):
    """Run a ReportsGeneration pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.ReportsGeneration] = (
        const.PipelineRunStages.ReportsGeneration
    )
    generate_ods_reports: Literal[True] = Field(
        default=True,
        alias="generateODSReports",
    )
    report_type_name: const.ReportType = const.ReportType.Crystal
    report_formats_list: list[const.ReportFormat]
    ods_report_list: list[str]
    bo_groups_list: list[str]
    run_mode: Literal[const.PipelineRunMode.Full, const.PipelineRunMode.Positions] = (
        const.PipelineRunMode.Full
    )


class UndoPost(_PipelineRunJob):
    """Run a UndoPost pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.UndoPost] = (
        const.PipelineRunStages.UndoPost
    )


class UndoFinalize(_PipelineRunJob):
    """Run a UndoFinalize pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.UndoFinalize] = (
        const.PipelineRunStages.UndoFinalize
    )


class CleanupDefferedResults(_PipelineRunJob):
    """Run a CleanupDefferedResults pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.CleanupDefferedResults] = (
        const.PipelineRunStages.CleanupDefferedResults
    )


class UpdateAnalytics(_PipelineRunJob):
    """Run a UpdateAnalytics pipeline."""

    stage_type_seq: Literal[const.PipelineRunStages.UpdateAnalytics] = (
        const.PipelineRunStages.UpdateAnalytics
    )


class _ImportJob(_PipelineJob):
    """Base class for an Import job."""

    command: Literal["Import"] = "Import"
    stage_type_seq: const.ImportStages
    calendar_seq: str
    batch_name: str
    module: const.StageTables
    run_mode: const.ImportRunMode = const.ImportRunMode.All

    @computed_field
    def stage_tables(self) -> list[str]:
        """Compute stageTables field based on module."""
        return STAGETABLES[self.module]

    @model_validator(mode="after")
    def validate_conditional_fields(self) -> "_ImportJob":
        """Validate conditional required fields.

        Validations:
        -----------
        - run_mode can only be 'new' when importing TransactionalData
        """
        if (
            self.module != const.StageTables.TransactionalData
            and self.run_mode == const.ImportRunMode.New
        ):
            raise ValueError(
                "run_mode can only be 'new' when importing TransactionalData"
            )

        return self


class Validate(_ImportJob):
    """Run a Validate pipeline."""

    stage_type_seq: Literal[const.ImportStages.Validate] = const.ImportStages.Validate
    revalidate: const.RevalidateMode = const.RevalidateMode.All


class Transfer(_ImportJob):
    """Run a Transfer pipeline."""

    stage_type_seq: Literal[const.ImportStages.Transfer] = const.ImportStages.Transfer


class ValidateAndTransfer(_ImportJob):
    """Run a ValidateAndTransfer pipeline."""

    stage_type_seq: Literal[const.ImportStages.ValidateAndTransfer] = (
        const.ImportStages.ValidateAndTransfer
    )
    revalidate: const.RevalidateMode = const.RevalidateMode.All


class ValidateAndTransferIfAllValid(_ImportJob):
    """Run a ValidateAndTransferIfAllValid pipeline."""

    stage_type_seq: Literal[const.ImportStages.ValidateAndTransferIfAllValid] = (
        const.ImportStages.ValidateAndTransferIfAllValid
    )
    revalidate: const.RevalidateMode = const.RevalidateMode.All


class TransferIfAllValid(_ImportJob):
    """Run a TransferIfAllValid pipeline."""

    stage_type_seq: Literal[const.ImportStages.TransferIfAllValid] = (
        const.ImportStages.TransferIfAllValid
    )
