"""Constants for Python SAP Commissions Client."""

from enum import StrEnum
from typing import Final


class HTTPMETHOD(StrEnum):
    """StrEnum for HTTP request methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


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

    FULL = "full"
    POSITIONS = "positions"
    INCREMENTAL = "incremental"


class ImportRunMode(StrEnum):
    """StrEnum for Import RunMode."""

    ALL = "all"
    NEW = "new"


class RevalidateMode(StrEnum):
    """StrEnum for Import Revalidate."""

    ALL = "all"
    ERRORS = "onlyError"


class PipelineState(StrEnum):
    """StrEnum for Pipeline state."""

    SCHEDULED = "Scheduled"
    RUNNING = "Running"
    DONE = "Done"
    PENDING = "Pending"


class PipelineStatus(StrEnum):
    """StrEnum for Pipeline status."""

    RUNNING = "Running"
    SUCCESSFUL = "Successful"
    CANCELED = "Cancel"
    DONE = "Done"
    FAILED = "Failed"
    _Cacel = "Cacel"


REQUEST_TIMEOUT: Final[int] = 30
STATUS_NOT_MODIFIED: Final[int] = 304
STATUS_BAD_REQUEST: Final[int] = 400
STATUS_SERVER_ERROR: Final[int] = 500
REQUIRED_STATUS: Final[dict[str, tuple[int]]] = {
    "GET": (200,),
    "POST": (200, 201, STATUS_NOT_MODIFIED),
    "PUT": (200, STATUS_NOT_MODIFIED),
    "DELETE": (200,),
}

ATTR_ERROR: Final[str] = "_ERROR_"
ATTR_EXPAND: Final[str] = "expand"
ATTR_FILTER: Final[str] = "$filter"
ATTR_ORDERBY: Final[str] = "orderBy"
ATTR_INLINECOUNT: Final[str] = "inlineCount"
ATTR_NEXT: Final[str] = "next"
ATTR_SKIP: Final[str] = "skip"
ATTR_TOP: Final[str] = "top"
ATTR_TOTAL: Final[str] = "total"

ERROR_ALREADY_EXISTS: Final[str] = "TCMP_35004"
ERROR_DELETE_PIPELINE: Final[str] = "TCMP_60255"
ERROR_MISSING_FIELD: Final[str] = "TCMP_1002"
ERROR_NOT_FOUND: Final[str] = "TCMP_09007"
ERROR_REFERRED_BY: Final[str] = "TCMP_35001"
ERROR_REMOVE_FAILED: Final[str] = "TCMP_35243"

MSG_PERIOD_TYPE: Final[str] = "Period Type mismatch"
MSG_SUCCESS_DELETE: Final[str] = "successfully deleted"

MAX_ATTEMPTS: Final[int] = 3
MAX_PAGE_SIZE: Final[int] = 100

STAGETABLES: Final[dict[str, list[str]]] = {
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
