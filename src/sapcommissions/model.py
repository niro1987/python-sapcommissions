"""Data models for Python SAP Commissions Client."""

from datetime import datetime
from typing import Literal

import pydantic

from sapcommissions import const

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


class ValueUnitType(pydantic.BaseModel):
    """BaseModel for UnitType."""

    name: str
    unitTypeSeq: str


class Value(pydantic.BaseModel):
    """BaseModel for Value."""

    value: int | float
    unitType: ValueUnitType


class RuleUsage(pydantic.BaseModel):
    """BaseModel for RuleUsage."""

    id: str
    name: str


class _Base(pydantic.BaseModel):
    """BaseModel."""

    _endpoint: str
    _attr_seq: str

    @classmethod
    def get_endpoint(cls) -> str:
        """Return the class endpoint."""
        return cls.__private_attributes__["_endpoint"].default

    @classmethod
    def get_attr_seq(cls) -> str:
        """Return the seq attribute name."""
        return cls.__private_attributes__["_attr_seq"].default

    @property
    def seq(self) -> str | None:
        """Return the `seq` attribute value for the resource."""
        return getattr(self, self._attr_seq)


class _Resource(_Base):
    """Base class for a Resource."""

    createDate: datetime | None = pydantic.Field(None, exclude=True, repr=False)
    createdBy: str | None = pydantic.Field(None, exclude=True, repr=False)
    modifiedBy: str | None = pydantic.Field(None, exclude=True, repr=False)


class _DataType(_Resource):
    """Base class for Data Type resources."""

    _attr_seq: str = "dataTypeSeq"
    dataTypeSeq: str | None = None
    description: str | None = pydantic.Field(
        None, validation_alias=pydantic.AliasChoices("description", "Description")
    )
    notAllowUpdate: bool | None = pydantic.Field(None, repr=False)


class _RuleElement(_Resource):
    """Base class for Rule Element resources."""

    _attr_seq: str = "ruleElementSeq"
    ruleElementSeq: str | None = None


class _RuleElementOwner(_Resource):
    """Base class for Rule Element Owner resources."""

    _attr_seq: str = "ruleElementOwnerSeq"
    ruleElementOwnerSeq: str | None = None


class _Pipeline(_Base):
    """Base class for Pipeline resources."""

    _endpoint: str = "api/v2/pipelines"
    _attr_seq: str = "pipelineRunSeq"
    pipelineRunSeq: str | None = None


class _PipelineJob(_Pipeline):
    """Base class for a Pipeline Job."""

    command: Literal["PipelineRun", "Import", "XMLImport", "ModelRun", "MaintenanceRun"]
    pipelineRunSeq: None = None
    runStats: bool = False


class _PipelineRunJob(_PipelineJob):
    """Base class for a PipelineRun job."""

    command: Literal["PipelineRun"] = "PipelineRun"
    periodSeq: str
    calendarSeq: str
    stageTypeSeq: const.PipelineRunStages
    runMode: const.PipelineRunMode = const.PipelineRunMode.Full
    positionGroups: list[str] | None = None
    positionSeqs: list[str] | None = None
    processingUnitSeq: str | None = None

    @pydantic.model_validator(mode="after")
    def check_runmode(self) -> "_PipelineRunJob":
        """If runMode is 'positions', positionGroups or positionSeqs must be list."""
        if self.runMode in (
            const.PipelineRunMode.Full,
            const.PipelineRunMode.Incremental,
        ):
            if not (self.positionGroups is None and self.positionSeqs is None):
                raise ValueError(
                    "When runMode is 'full' or 'incremental', positionGroups and positionSeqs must be None"
                )

        if self.runMode == const.PipelineRunMode.Positions:
            if not (self.positionGroups and self.positionSeqs) or (
                self.positionGroups and self.positionSeqs
            ):
                raise ValueError(
                    "When runMode is 'positions', provide either positionGroups or positionSeqs"
                )
            if isinstance(self.positionGroups, list) and not len(self.positionGroups):
                raise ValueError("positionGroups cannot be an empty list")
            if isinstance(self.positionSeqs, list) and not len(self.positionSeqs):
                raise ValueError("positionSeqs cannot be an empty list")
        return self


class EventType(_DataType):
    """Class representation of an Event Type."""

    _endpoint: str = "api/v2/eventTypes"
    eventTypeId: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("eventTypeId", "ID")
    )


class CreditType(_DataType):
    """Credit Type."""

    _endpoint: str = "api/v2/creditTypes"
    creditTypeId: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("creditTypeId", "ID", "Credit Type ID")
    )


class EarningCode(_DataType):
    """Earning Code."""

    _endpoint: str = "api/v2/earningCodes"
    earningCodeId: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("earningCodeId", "ID")
    )


class EarningGroup(_DataType):
    """Earning Group."""

    _endpoint: str = "api/v2/earningGroups"
    earningGroupId: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("earningGroupId", "ID")
    )


class FixedValueType(_DataType):
    """Fixed Value Type."""

    _endpoint: str = "api/v2/fixedValueTypes"
    fixedValueTypeId: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("fixedValueTypeId", "ID")
    )


class ReasonCode(_DataType):
    """Reason Code."""

    _endpoint: str = "api/v2/reasons"
    reasonId: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("reasonId", "ID")
    )


class BusinessUnit(_Resource):
    """Business Unit."""

    _endpoint: str = "api/v2/businessUnits"
    _attr_seq: str = "businessUnitSeq"
    businessUnitSeq: str | None = None
    name: str
    description: str | None = None
    processingUnit: str | None = None


class ProcessingUnit(_Resource):
    """Processing Unit."""

    _endpoint: str = "api/v2/processingUnits"
    _attr_seq: str = "processingUnitSeq"
    processingUnitSeq: str | None = None
    name: str
    description: str | None = None


class PeriodType(_Resource):
    """Period Type."""

    _endpoint: str = "api/v2/periodTypes"
    _attr_seq: str = "periodTypeSeq"
    periodTypeSeq: str | None = None
    name: str
    description: str | None = None
    level: int | None = None


class Calendar(_Resource):
    """Calendar."""

    _endpoint: str = "api/v2/calendars"
    _attr_seq: str = "calendarSeq"
    calendarSeq: str | None = None
    name: str
    description: str | None = None
    minorPeriodType: str | None = None
    majorPeriodType: str | None = None
    periods: list[str] | None = None


class Period(_Resource):
    """Period."""

    _endpoint: str = "api/v2/periods"
    _attr_seq: str = "periodSeq"
    periodSeq: str | None = None
    name: str
    shortName: str
    startDate: datetime
    endDate: datetime
    periodType: str
    calendar: str
    description: str | None = None
    parent: str | None = None


class Assignment(pydantic.BaseModel):
    """BaseModel for Assignment."""

    key: str | None = None
    ownedKey: str | None = None


class Title(_RuleElementOwner):
    """Title."""

    _endpoint: str = "api/v2/titles"
    name: str
    description: str | None = None
    effectiveStartDate: datetime
    effectiveEndDate: datetime
    businessUnits: list[str] | None = None
    plan: str | None = None
    variableAssignments: Assignment | list[Assignment | str] | None = None
    modelSeq: str | None = None
    ga1: str | None = pydantic.Field(None, alias="genericAttribute1")
    ga2: str | None = pydantic.Field(None, alias="genericAttribute2")
    ga3: str | None = pydantic.Field(None, alias="genericAttribute3")
    ga4: str | None = pydantic.Field(None, alias="genericAttribute4")
    ga5: str | None = pydantic.Field(None, alias="genericAttribute5")
    ga6: str | None = pydantic.Field(None, alias="genericAttribute6")
    ga7: str | None = pydantic.Field(None, alias="genericAttribute7")
    ga8: str | None = pydantic.Field(None, alias="genericAttribute8")
    ga9: str | None = pydantic.Field(None, alias="genericAttribute9")
    ga10: str | None = pydantic.Field(None, alias="genericAttribute10")
    ga11: str | None = pydantic.Field(None, alias="genericAttribute11")
    ga12: str | None = pydantic.Field(None, alias="genericAttribute12")
    ga13: str | None = pydantic.Field(None, alias="genericAttribute13")
    ga14: str | None = pydantic.Field(None, alias="genericAttribute14")
    ga15: str | None = pydantic.Field(None, alias="genericAttribute15")
    ga16: str | None = pydantic.Field(None, alias="genericAttribute16")
    gn1: Value | None = pydantic.Field(None, alias="genericNumber1")
    gn2: Value | None = pydantic.Field(None, alias="genericNumber2")
    gn3: Value | None = pydantic.Field(None, alias="genericNumber3")
    gn4: Value | None = pydantic.Field(None, alias="genericNumber4")
    gn5: Value | None = pydantic.Field(None, alias="genericNumber5")
    gn6: Value | None = pydantic.Field(None, alias="genericNumber6")
    gd1: datetime | None = pydantic.Field(None, alias="genericDate1")
    gd2: datetime | None = pydantic.Field(None, alias="genericDate2")
    gd3: datetime | None = pydantic.Field(None, alias="genericDate3")
    gd4: datetime | None = pydantic.Field(None, alias="genericDate4")
    gd5: datetime | None = pydantic.Field(None, alias="genericDate5")
    gd6: datetime | None = pydantic.Field(None, alias="genericDate6")
    gb1: bool | None = pydantic.Field(None, alias="genericBoolean1")
    gb2: bool | None = pydantic.Field(None, alias="genericBoolean2")
    gb3: bool | None = pydantic.Field(None, alias="genericBoolean3")
    gb4: bool | None = pydantic.Field(None, alias="genericBoolean4")
    gb5: bool | None = pydantic.Field(None, alias="genericBoolean5")
    gb6: bool | None = pydantic.Field(None, alias="genericBoolean6")


class Position(_RuleElementOwner):
    """Position."""

    _endpoint: str = "api/v2/positions"
    name: str
    description: str | None = None
    effectiveStartDate: datetime
    effectiveEndDate: datetime
    creditStartDate: datetime | None = None
    creditEndDate: datetime | None = None
    processingStartDate: datetime | None = None
    processingEndDate: datetime | None = None
    targetCompensation: dict | None = None
    processingUnit: str | None = None
    businessUnits: list[str] | None = None
    manager: str | None = None
    title: str | None = None
    plan: str | None = None
    positionGroup: str | None = None
    payee: str | None = None
    variableAssignments: Assignment | list[Assignment] | None = None
    modelSeq: str | None = None
    ga1: str | None = pydantic.Field(None, alias="genericAttribute1")
    ga2: str | None = pydantic.Field(None, alias="genericAttribute2")
    ga3: str | None = pydantic.Field(None, alias="genericAttribute3")
    ga4: str | None = pydantic.Field(None, alias="genericAttribute4")
    ga5: str | None = pydantic.Field(None, alias="genericAttribute5")
    ga6: str | None = pydantic.Field(None, alias="genericAttribute6")
    ga7: str | None = pydantic.Field(None, alias="genericAttribute7")
    ga8: str | None = pydantic.Field(None, alias="genericAttribute8")
    ga9: str | None = pydantic.Field(None, alias="genericAttribute9")
    ga10: str | None = pydantic.Field(None, alias="genericAttribute10")
    ga11: str | None = pydantic.Field(None, alias="genericAttribute11")
    ga12: str | None = pydantic.Field(None, alias="genericAttribute12")
    ga13: str | None = pydantic.Field(None, alias="genericAttribute13")
    ga14: str | None = pydantic.Field(None, alias="genericAttribute14")
    ga15: str | None = pydantic.Field(None, alias="genericAttribute15")
    ga16: str | None = pydantic.Field(None, alias="genericAttribute16")
    gn1: Value | None = pydantic.Field(None, alias="genericNumber1")
    gn2: Value | None = pydantic.Field(None, alias="genericNumber2")
    gn3: Value | None = pydantic.Field(None, alias="genericNumber3")
    gn4: Value | None = pydantic.Field(None, alias="genericNumber4")
    gn5: Value | None = pydantic.Field(None, alias="genericNumber5")
    gn6: Value | None = pydantic.Field(None, alias="genericNumber6")
    gd1: datetime | None = pydantic.Field(None, alias="genericDate1")
    gd2: datetime | None = pydantic.Field(None, alias="genericDate2")
    gd3: datetime | None = pydantic.Field(None, alias="genericDate3")
    gd4: datetime | None = pydantic.Field(None, alias="genericDate4")
    gd5: datetime | None = pydantic.Field(None, alias="genericDate5")
    gd6: datetime | None = pydantic.Field(None, alias="genericDate6")
    gb1: bool | None = pydantic.Field(None, alias="genericBoolean1")
    gb2: bool | None = pydantic.Field(None, alias="genericBoolean2")
    gb3: bool | None = pydantic.Field(None, alias="genericBoolean3")
    gb4: bool | None = pydantic.Field(None, alias="genericBoolean4")
    gb5: bool | None = pydantic.Field(None, alias="genericBoolean5")
    gb6: bool | None = pydantic.Field(None, alias="genericBoolean6")


class PositionGroup(_Resource):
    """Position."""

    _endpoint: str = "api/v2/positionGroups"
    _attr_seq: str = "positionGroupSeq"
    positionGroupSeq: str | None = None
    name: str
    businessUnits: list[str] | None = None


class AppliedDeposit(_Resource):
    """AppliedDeposit."""

    _endpoint: str = "api/v2/appliedDeposits"
    _attr_seq: str = "appliedDepositSeq"
    appliedDepositSeq: str | None = None
    position: str
    payee: str
    period: str
    earningGroupId: str
    earningCodeId: str
    trialPipelineRun: str
    trialPipelineRunDate: datetime
    postPipelineRun: str
    postPipelineRunDate: datetime
    entryNumber: str
    value: Value
    processingUnit: str | None = None


class Balance(_Resource):
    """Balance."""

    _endpoint: str = "api/v2/balances"
    _attr_seq: str = "balanceSeq"
    balanceSeq: str | None = None
    position: str
    payee: str
    period: str
    earningGroupId: str
    earningCodeId: str
    trialPipelineRun: str
    trialPipelineRunDate: datetime
    applyPipelineRun: str
    applyPipelineRunDate: datetime
    postPipelineRun: str
    postPipelineRunDate: datetime
    balanceStatusId: str
    value: Value
    processingUnit: str | None = None


class Category(_RuleElement):
    """Category."""

    _endpoint: str = "api/v2/categories"
    name: str
    description: str | None = None
    owner: str
    parent: str | None = None
    returnType: str | None = None
    effectiveStartDate: datetime
    effectiveEndDate: datetime
    businessUnits: list[str] | None = None
    ruleUsage: RuleUsage | None = None
    owningElement: str | None = None
    calendar: str | None = None
    inputSignature: str | None = None
    modelSeq: str | None = None
    ga1: str | None = pydantic.Field(None, alias="genericAttribute1")
    ga2: str | None = pydantic.Field(None, alias="genericAttribute2")
    ga3: str | None = pydantic.Field(None, alias="genericAttribute3")
    ga4: str | None = pydantic.Field(None, alias="genericAttribute4")
    ga5: str | None = pydantic.Field(None, alias="genericAttribute5")
    ga6: str | None = pydantic.Field(None, alias="genericAttribute6")
    ga7: str | None = pydantic.Field(None, alias="genericAttribute7")
    ga8: str | None = pydantic.Field(None, alias="genericAttribute8")
    ga9: str | None = pydantic.Field(None, alias="genericAttribute9")
    ga10: str | None = pydantic.Field(None, alias="genericAttribute10")
    ga11: str | None = pydantic.Field(None, alias="genericAttribute11")
    ga12: str | None = pydantic.Field(None, alias="genericAttribute12")
    ga13: str | None = pydantic.Field(None, alias="genericAttribute13")
    ga14: str | None = pydantic.Field(None, alias="genericAttribute14")
    ga15: str | None = pydantic.Field(None, alias="genericAttribute15")
    ga16: str | None = pydantic.Field(None, alias="genericAttribute16")
    gn1: Value | None = pydantic.Field(None, alias="genericNumber1")
    gn2: Value | None = pydantic.Field(None, alias="genericNumber2")
    gn3: Value | None = pydantic.Field(None, alias="genericNumber3")
    gn4: Value | None = pydantic.Field(None, alias="genericNumber4")
    gn5: Value | None = pydantic.Field(None, alias="genericNumber5")
    gn6: Value | None = pydantic.Field(None, alias="genericNumber6")
    gd1: datetime | None = pydantic.Field(None, alias="genericDate1")
    gd2: datetime | None = pydantic.Field(None, alias="genericDate2")
    gd3: datetime | None = pydantic.Field(None, alias="genericDate3")
    gd4: datetime | None = pydantic.Field(None, alias="genericDate4")
    gd5: datetime | None = pydantic.Field(None, alias="genericDate5")
    gd6: datetime | None = pydantic.Field(None, alias="genericDate6")
    gb1: bool | None = pydantic.Field(None, alias="genericBoolean1")
    gb2: bool | None = pydantic.Field(None, alias="genericBoolean2")
    gb3: bool | None = pydantic.Field(None, alias="genericBoolean3")
    gb4: bool | None = pydantic.Field(None, alias="genericBoolean4")
    gb5: bool | None = pydantic.Field(None, alias="genericBoolean5")
    gb6: bool | None = pydantic.Field(None, alias="genericBoolean6")


class categoryClassifier(_Resource):
    """categoryClassifier."""

    _endpoint: str = "api/v2/categoryClassifiers"
    _attr_seq: str = "categoryClassifiersSeq"
    categoryClassifiersSeq: str | None = None
    categoryTree: str
    category: str
    classifier: str
    effectiveStartDate: datetime
    effectiveEndDate: datetime


class CategoryTree(_Resource):
    """CategoryTree."""

    _endpoint: str = "api/v2/categoryTrees"
    _attr_seq: str = "categoryTreeSeq"
    categoryTreeSeq: str | None = None
    name: str
    description: str | None = None
    classifierSelectorId: str | None = None
    classifierClass: str
    effectiveStartDate: datetime
    effectiveEndDate: datetime
    businessUnits: list[str] | None = None


class Commission(_Resource):
    """Commission.

    TODO: No results.
    """

    _endpoint: str = "api/v2/commissions"
    _attr_seq: str = "commissionSeq"
    commissionSeq: str | None = None
    position: str
    payee: str
    period: str
    incentive: str
    credit: str
    pipelineRun: str
    pipelineRunDate: datetime
    value: Value
    rateValue: Value
    entryNumber: Value
    businessUnits: list[str] | None = None
    processingUnit: str = pydantic.Field(repr=False)
    isPrivate: bool | None = None
    originTypeId: str


class Credit(_Resource):
    """Credit."""

    _endpoint: str = "api/v2/credits"
    _attr_seq: str = "creditSeq"
    creditSeq: str | None = None
    name: str
    position: str
    payee: str
    salesOrder: str
    salesTransaction: str | None = None
    period: str
    creditType: str
    value: Value
    preadjustedValue: Value
    originTypeId: str
    reason: str | None = None
    rule: str | None = None
    isRollable: bool | None = None
    rollDate: datetime | None = None
    isHeld: bool | None = None
    releaseDate: datetime | None = None
    pipelineRun: str | None = None
    pipelineRunDate: datetime | None = None
    compensationDate: datetime | None = None
    comments: str | None = None
    isPrivate: bool | None = None
    modelSeq: str | None = None
    businessUnits: list[str] | None = None
    ga1: str | None = pydantic.Field(None, alias="genericAttribute1")
    ga2: str | None = pydantic.Field(None, alias="genericAttribute2")
    ga3: str | None = pydantic.Field(None, alias="genericAttribute3")
    ga4: str | None = pydantic.Field(None, alias="genericAttribute4")
    ga5: str | None = pydantic.Field(None, alias="genericAttribute5")
    ga6: str | None = pydantic.Field(None, alias="genericAttribute6")
    ga7: str | None = pydantic.Field(None, alias="genericAttribute7")
    ga8: str | None = pydantic.Field(None, alias="genericAttribute8")
    ga9: str | None = pydantic.Field(None, alias="genericAttribute9")
    ga10: str | None = pydantic.Field(None, alias="genericAttribute10")
    ga11: str | None = pydantic.Field(None, alias="genericAttribute11")
    ga12: str | None = pydantic.Field(None, alias="genericAttribute12")
    ga13: str | None = pydantic.Field(None, alias="genericAttribute13")
    ga14: str | None = pydantic.Field(None, alias="genericAttribute14")
    ga15: str | None = pydantic.Field(None, alias="genericAttribute15")
    ga16: str | None = pydantic.Field(None, alias="genericAttribute16")
    gn1: Value | None = pydantic.Field(None, alias="genericNumber1")
    gn2: Value | None = pydantic.Field(None, alias="genericNumber2")
    gn3: Value | None = pydantic.Field(None, alias="genericNumber3")
    gn4: Value | None = pydantic.Field(None, alias="genericNumber4")
    gn5: Value | None = pydantic.Field(None, alias="genericNumber5")
    gn6: Value | None = pydantic.Field(None, alias="genericNumber6")
    gd1: datetime | None = pydantic.Field(None, alias="genericDate1")
    gd2: datetime | None = pydantic.Field(None, alias="genericDate2")
    gd3: datetime | None = pydantic.Field(None, alias="genericDate3")
    gd4: datetime | None = pydantic.Field(None, alias="genericDate4")
    gd5: datetime | None = pydantic.Field(None, alias="genericDate5")
    gd6: datetime | None = pydantic.Field(None, alias="genericDate6")
    gb1: bool | None = pydantic.Field(None, alias="genericBoolean1")
    gb2: bool | None = pydantic.Field(None, alias="genericBoolean2")
    gb3: bool | None = pydantic.Field(None, alias="genericBoolean3")
    gb4: bool | None = pydantic.Field(None, alias="genericBoolean4")
    gb5: bool | None = pydantic.Field(None, alias="genericBoolean5")
    gb6: bool | None = pydantic.Field(None, alias="genericBoolean6")
    processingUnit: str = pydantic.Field(repr=False)


class ResetFromValidate(_Pipeline):
    """Run a ResetFromValidate pipeline."""

    _endpoint: str = "api/v2/pipelines/resetfromvalidate"
    pipelineRunSeq: None = None
    calendarSeq: str
    periodSeq: str
    batchName: str | None = None
    runStats: bool = False


class Purge(_Pipeline):
    """Run a Purge pipeline."""

    _endpoint: str = "api/v2/pipelines"
    pipelineRunSeq: None = None
    command: Literal["PipelineRun"] = "PipelineRun"
    stageTypeSeq: Literal[const.PipelineRunStages.Purge] = const.PipelineRunStages.Purge
    batchName: str
    module: const.StageTables

    @pydantic.computed_field
    def stageTables(self) -> list[str]:
        """Compute stageTables field based on module."""
        return STAGETABLES[self.module]


class Pipeline(_Pipeline):
    """Pipeline."""

    pipelineRunSeq: str
    command: (
        Literal[
            "PipelineRun",
            "Import",
            "XMLImport",
            "ModelRun",
            "MaintenanceRun",
            "CleanupDeferredPipelineResults",
        ]
        | None
    )
    stageType: (
        const.PipelineRunStages
        | const.ImportStages
        | const.XMLImportStages
        | const.MaintenanceStages
        | None
    )
    dateSubmitted: datetime
    state: const.PipelineState
    userId: str
    processingUnit: str = pydantic.Field(repr=False)
    period: str | None = None
    description: str | None = None
    status: const.PipelineStatus | None = None
    runProgress: float | None = None
    startTime: datetime | None = pydantic.Field(None, repr=False)
    stopTime: datetime | None = pydantic.Field(None, repr=False)
    startDateScheduled: datetime | None = pydantic.Field(None, repr=False)
    batchName: str | None = None
    priority: int | None = pydantic.Field(repr=False)
    message: str | None = pydantic.Field(None, repr=False)
    numErrors: int | None = pydantic.Field(repr=False)
    numWarnings: int | None = pydantic.Field(repr=False)
    runMode: const.ImportRunMode | const.PipelineRunMode | None = pydantic.Field(
        None, repr=False
    )

    @pydantic.field_validator("runProgress", mode="before")
    @classmethod
    def percent_as_float(cls, value: str) -> float | None:
        """Convert percentage string to float."""
        return int(value.removesuffix("%")) / 100 if value else None


class Classify(_PipelineRunJob):
    """Run a Classify pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.Classify] = (
        const.PipelineRunStages.Classify
    )
    runMode: Literal[const.PipelineRunMode.Full, const.PipelineRunMode.Incremental] = (
        const.PipelineRunMode.Full
    )
    positionGroups: None = None
    positionSeqs: None = None


class Allocate(_PipelineRunJob):
    """Run an Allocate pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.Allocate] = (
        const.PipelineRunStages.Allocate
    )


class Reward(_PipelineRunJob):
    """Run a Reward pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.Reward] = (
        const.PipelineRunStages.Reward
    )
    runMode: Literal[const.PipelineRunMode.Full, const.PipelineRunMode.Positions] = (
        const.PipelineRunMode.Full
    )


class Pay(_PipelineRunJob):
    """Run a Pay pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.Pay] = const.PipelineRunStages.Pay
    runMode: Literal[const.PipelineRunMode.Full, const.PipelineRunMode.Positions] = (
        const.PipelineRunMode.Full
    )
    positionSeqs: None = None


class Summarize(_PipelineRunJob):
    """Run a Summarize pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.Summarize] = (
        const.PipelineRunStages.Summarize
    )


class Compensate(_PipelineRunJob):
    """Run a Compensate pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.Compensate] = (
        const.PipelineRunStages.Compensate
    )
    removeStaleResults: bool = False


class CompensateAndPay(_PipelineRunJob):
    """Run a CompensateAndPay pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.CompensateAndPay] = (
        const.PipelineRunStages.CompensateAndPay
    )
    removeStaleResults: bool = False


class ResetFromClassify(_PipelineRunJob):
    """Run a ResetFromClassify pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.ResetFromClassify] = (
        const.PipelineRunStages.ResetFromClassify
    )


class ResetFromAllocate(_PipelineRunJob):
    """Run a ResetFromAllocate pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.ResetFromAllocate] = (
        const.PipelineRunStages.ResetFromAllocate
    )


class ResetFromReward(_PipelineRunJob):
    """Run a ResetFromReward pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.ResetFromReward] = (
        const.PipelineRunStages.ResetFromReward
    )


class ResetFromPay(_PipelineRunJob):
    """Run a ResetFromPay pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.ResetFromPay] = (
        const.PipelineRunStages.ResetFromPay
    )


class Post(_PipelineRunJob):
    """Run a Post pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.Post] = const.PipelineRunStages.Post


class Finalize(_PipelineRunJob):
    """Run a Finalize pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.Finalize] = (
        const.PipelineRunStages.Finalize
    )


class ReportsGeneration(_PipelineRunJob):
    """Run a ReportsGeneration pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.ReportsGeneration] = (
        const.PipelineRunStages.ReportsGeneration
    )
    generateODSReports: Literal[True] = True
    reportTypeName: const.ReportType = const.ReportType.Crystal
    reportFormatsList: list[const.ReportFormat]
    odsReportList: list[str]
    boGroupsList: list[str]
    runMode: Literal[const.PipelineRunMode.Full, const.PipelineRunMode.Positions] = (
        const.PipelineRunMode.Full
    )


class UndoPost(_PipelineRunJob):
    """Run a UndoPost pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.UndoPost] = (
        const.PipelineRunStages.UndoPost
    )


class UndoFinalize(_PipelineRunJob):
    """Run a UndoFinalize pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.UndoFinalize] = (
        const.PipelineRunStages.UndoFinalize
    )


class CleanupDefferedResults(_PipelineRunJob):
    """Run a CleanupDefferedResults pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.CleanupDefferedResults] = (
        const.PipelineRunStages.CleanupDefferedResults
    )


class UpdateAnalytics(_PipelineRunJob):
    """Run a UpdateAnalytics pipeline."""

    stageTypeSeq: Literal[const.PipelineRunStages.UpdateAnalytics] = (
        const.PipelineRunStages.UpdateAnalytics
    )


class _XMLImportJob(_PipelineJob):
    """Base class for an XMLImport Pipeline job."""

    command: Literal["XMLImport"] = "XMLImport"
    stageTypeSeq: const.XMLImportStages


class XMLImport(_XMLImportJob):
    """Run an XML Import pipeline."""

    stageTypeSeq: Literal[const.XMLImportStages.XMLImport] = (
        const.XMLImportStages.XMLImport
    )
    xmlFileName: str
    xmlFileContent: str
    updateExistingObjects: bool = False


class _ImportJob(_PipelineJob):
    """Base class for an Import job."""

    command: Literal["Import"] = "Import"
    stageTypeSeq: const.ImportStages
    calendarSeq: str
    batchName: str
    module: const.StageTables
    runMode: const.ImportRunMode = const.ImportRunMode.All

    @pydantic.computed_field
    def stageTables(self) -> list[str]:
        """Compute stageTables field based on module."""
        return STAGETABLES[self.module]

    @pydantic.model_validator(mode="after")
    def validate_conditional_fields(self) -> "_ImportJob":
        """Validate conditional required fields.

        Validations:
        -----------
        - runMode can only be 'new' when importing TransactionalData
        """
        if (
            self.module != const.StageTables.TransactionalData
            and self.runMode == const.ImportRunMode.New
        ):
            raise ValueError(
                "runMode can only be 'new' when importing TransactionalData"
            )

        return self


class Validate(_ImportJob):
    """Run a Validate pipeline."""

    stageTypeSeq: Literal[const.ImportStages.Validate] = const.ImportStages.Validate
    revalidate: const.RevalidateMode = const.RevalidateMode.All


class Transfer(_ImportJob):
    """Run a Transfer pipeline."""

    stageTypeSeq: Literal[const.ImportStages.Transfer] = const.ImportStages.Transfer


class ValidateAndTransfer(_ImportJob):
    """Run a ValidateAndTransfer pipeline."""

    stageTypeSeq: Literal[const.ImportStages.ValidateAndTransfer] = (
        const.ImportStages.ValidateAndTransfer
    )
    revalidate: const.RevalidateMode = const.RevalidateMode.All


class ValidateAndTransferIfAllValid(_ImportJob):
    """Run a ValidateAndTransferIfAllValid pipeline."""

    stageTypeSeq: Literal[const.ImportStages.ValidateAndTransferIfAllValid] = (
        const.ImportStages.ValidateAndTransferIfAllValid
    )
    revalidate: const.RevalidateMode = const.RevalidateMode.All


class TransferIfAllValid(_ImportJob):
    """Run a TransferIfAllValid pipeline."""

    stageTypeSeq: Literal[const.ImportStages.TransferIfAllValid] = (
        const.ImportStages.TransferIfAllValid
    )
