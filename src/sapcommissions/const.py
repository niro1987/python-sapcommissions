"""Constants for Python SAP Commissions Client."""

from enum import StrEnum


class PipelineRunStages(StrEnum):
    """StrEnum for PipelineRun stages."""

    Classify = "21673573206720515"
    Allocate = "21673573206720516"
    Reward = "21673573206720518"
    Pay = "21673573206720519"
    Summarize = "21673573206720531"
    Compensate = "21673573206720530"
    CompensateAndPay = "21673573206720532"
    ResetFromClassify = "21673573206720514"
    ResetFromAllocate = "21673573206720523"
    ResetFromReward = "21673573206720522"
    ResetFromPay = "21673573206720526"
    Post = "21673573206720520"
    Finalize = "21673573206720521"
    Purge = "21673573206720573"
    ReportsGeneration = "21673573206720698"
    UndoPost = "21673573206720718"
    UndoFinalize = "21673573206720721"
    CleanupDefferedResults = "21673573206720540"
    UpdateAnalytics = "21673573206720701"


class ImportStages(StrEnum):
    """StrEnum for Import stages."""

    Validate = "21673573206720533"
    Transfer = "21673573206720534"
    ValidateAndTransfer = "21673573206720536"
    ValidateAndTransferIfAllValid = "21673573206720537"
    TransferIfAllValid = "21673573206720535"
    ResetFromValidate = "21673573206720525"


class XMLImportStages(StrEnum):
    """StrEnum for XMLImport stage."""

    XMLImport = "21673573206720693"


class MaintenanceStages(StrEnum):
    """StrEnum for Maintenance stage."""

    Maintenance = "21673573206720692"


class StageTables(StrEnum):
    """StrEnum for StageTables."""

    TransactionalData = "TransactionalData"
    OrganizationData = "OrganizationData"
    ClassificationData = "ClassificationData"
    PlanRelatedData = "PlanRelatedData"


class ReportType(StrEnum):
    """StrEnum for ReportType."""

    Crystal = "Crystal"
    WebI = "Webi"


class ReportFormat(StrEnum):
    """StrEnum for ReportFormat."""

    Native = "native"
    Excel = "excel"
    PDF = "pdf"


class PipelineRunMode(StrEnum):
    """StrEnum for PipelineRun RunMode."""

    Full = "full"
    Positions = "positions"
    Incremental = "incremental"


class ImportRunMode(StrEnum):
    """StrEnum for Import RunMode."""

    All = "all"
    New = "new"


class RevalidateMode(StrEnum):
    """StrEnum for Import Revalidate."""

    All = "all"
    Errors = "onlyError"


class PipelineState(StrEnum):
    """StrEnum for Pipeline state."""

    Scheduled = "Scheduled"
    Running = "Running"
    Done = "Done"
    Pending = "Pending"


class PipelineStatus(StrEnum):
    """StrEnum for Pipeline status."""

    Running = "Running"
    Successful = "Successful"
    Cancel = "Cancel"
    Done = "Done"
    Failed = "Failed"
    _Cacel = "Cacel"
