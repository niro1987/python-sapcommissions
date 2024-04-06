"""Data models for Python SAP Commissions Client."""

from datetime import datetime
from typing import ClassVar, Literal

import pydantic
from pydantic.alias_generators import to_camel

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


class _BaseModel(pydantic.BaseModel):
    """BaseModel for SAP Commissions."""

    model_config: ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
        str_strip_whitespace=True,
        str_min_length=1,
        extra="allow",
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
        alias_generator=pydantic.AliasGenerator(alias=to_camel),
    )


class Assignment(_BaseModel):
    """BaseModel for Assignment."""

    key: str | None = None
    owned_key: str | None = None


class ValueUnitType(_BaseModel):
    """BaseModel for UnitType."""

    name: str
    unit_type_seq: str


class Value(_BaseModel):
    """BaseModel for Value."""

    value: int | float
    unit_type: ValueUnitType


class RuleUsage(_BaseModel):
    """BaseModel for RuleUsage."""

    id: str
    name: str


class _Endpoint(_BaseModel):
    """BaseModel for an Endpoint."""

    _endpoint: ClassVar[str]

    @classmethod
    def get_endpoint(cls) -> str:
        """Return the class endpoint."""
        return cls._endpoint


class _Resource(_Endpoint):
    """Base class for a Resource."""

    _attr_seq: ClassVar[str]
    create_date: datetime | None = pydantic.Field(None, exclude=True, repr=False)
    created_by: str | None = pydantic.Field(None, exclude=True, repr=False)
    modified_by: str | None = pydantic.Field(None, exclude=True, repr=False)

    @classmethod
    def get_attr_seq(cls) -> str:
        """Return the seq attribute name."""
        return cls._attr_seq

    @property
    def seq(self) -> str | None:
        """Return the `seq` attribute value for the resource."""
        return getattr(self, self._attr_seq)


class _DataType(_Resource):
    """Base class for Data Type resources."""

    _attr_seq: ClassVar[str] = "data_type_seq"
    data_type_seq: str | None = None
    description: str | None = pydantic.Field(
        None,
        validation_alias=pydantic.AliasChoices("description", "Description"),
    )
    not_allow_update: bool | None = pydantic.Field(None, repr=False)


class _RuleElement(_Resource):
    """Base class for Rule Element resources."""

    _attr_seq: ClassVar[str] = "rule_element_seq"
    rule_element_seq: str | None = None


class _RuleElementOwner(_Resource):
    """Base class for Rule Element Owner resources."""

    _attr_seq: ClassVar[str] = "rule_element_owner_seq"
    rule_element_owner_seq: str | None = None


class AppliedDeposit(_Resource):
    """AppliedDeposit."""

    _endpoint: ClassVar[str] = "api/v2/appliedDeposits"
    _attr_seq: ClassVar[str] = "applied_deposit_seq"
    applied_deposit_seq: str | None = None
    position: str
    payee: str
    period: str
    earning_group_id: str
    earning_code_id: str
    trial_pipeline_run: str
    trial_pipeline_run_date: datetime
    post_pipeline_run: str
    post_pipeline_run_date: datetime
    entry_number: str
    value: Value
    processing_unit: str | None = None


class Balance(_Resource):
    """Balance."""

    _endpoint: ClassVar[str] = "api/v2/balances"
    _attr_seq: ClassVar[str] = "balance_seq"
    balance_seq: str | None = None
    position: str
    payee: str
    period: str
    earning_group_id: str
    earning_code_id: str
    trial_pipeline_run: str
    trial_pipeline_run_date: datetime
    apply_pipeline_run: str
    apply_pipeline_run_date: datetime
    post_pipeline_run: str
    post_pipeline_run_date: datetime
    balance_status_id: str
    value: Value
    processing_unit: str | None = None


class BusinessUnit(_Resource):
    """Business Unit."""

    _endpoint: ClassVar[str] = "api/v2/businessUnits"
    _attr_seq: ClassVar[str] = "business_unit_seq"
    business_unit_seq: str | None = None
    name: str
    description: str | None = None
    processing_unit: str | None = None


class Calendar(_Resource):
    """Calendar."""

    _endpoint: ClassVar[str] = "api/v2/calendars"
    _attr_seq: ClassVar[str] = "calendar_seq"
    calendar_seq: str | None = None
    name: str
    description: str | None = None
    minor_period_type: str | None = None
    major_period_type: str | None = None
    periods: list[str] | None = None


class Category(_RuleElement):
    """Category."""

    _endpoint: ClassVar[str] = "api/v2/categories"
    name: str
    description: str | None = None
    owner: str
    parent: str | None = None
    return_type: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    rule_usage: RuleUsage | None = None
    owning_element: str | None = None
    calendar: str | None = None
    input_signature: str | None = None
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
    gd1: datetime | None = pydantic.Field(None, alias="generic_date1")
    gd2: datetime | None = pydantic.Field(None, alias="generic_date2")
    gd3: datetime | None = pydantic.Field(None, alias="generic_date3")
    gd4: datetime | None = pydantic.Field(None, alias="generic_date4")
    gd5: datetime | None = pydantic.Field(None, alias="generic_date5")
    gd6: datetime | None = pydantic.Field(None, alias="generic_date6")
    gb1: bool | None = pydantic.Field(None, alias="genericBoolean1")
    gb2: bool | None = pydantic.Field(None, alias="genericBoolean2")
    gb3: bool | None = pydantic.Field(None, alias="genericBoolean3")
    gb4: bool | None = pydantic.Field(None, alias="genericBoolean4")
    gb5: bool | None = pydantic.Field(None, alias="genericBoolean5")
    gb6: bool | None = pydantic.Field(None, alias="genericBoolean6")


class CategoryClassifier(_Resource):
    """categoryClassifier."""

    _endpoint: ClassVar[str] = "api/v2/categoryClassifiers"
    _attr_seq: ClassVar[str] = "category_classifiers_seq"
    category_classifiers_seq: str | None = None
    category_tree: str
    category: str
    classifier: str
    effective_start_date: datetime
    effective_end_date: datetime


class CategoryTree(_Resource):
    """CategoryTree."""

    _endpoint: ClassVar[str] = "api/v2/categoryTrees"
    _attr_seq: ClassVar[str] = "category_tree_seq"
    category_tree_seq: str | None = None
    name: str
    description: str | None = None
    classifier_selector_id: str | None = None
    classifier_class: str
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None


class Commission(_Resource):
    """Commission.

    TODO: No results.
    """

    _endpoint: ClassVar[str] = "api/v2/commissions"
    _attr_seq: ClassVar[str] = "commission_seq"
    commission_seq: str | None = None
    position: str
    payee: str
    period: str
    incentive: str
    credit: str
    pipeline_run: str
    pipeline_run_date: datetime
    value: Value
    rate_value: Value
    entry_number: Value
    business_units: list[str] | None = None
    processing_unit: str = pydantic.Field(repr=False)
    is_private: bool | None = None
    origin_type_id: str


class Credit(_Resource):
    """Credit."""

    _endpoint: ClassVar[str] = "api/v2/credits"
    _attr_seq: ClassVar[str] = "credit_seq"
    credit_seq: str | None = None
    name: str
    position: str
    payee: str
    sales_order: str
    sales_transaction: str | None = None
    period: str
    credit_type: str
    value: Value
    preadjusted_value: Value
    origin_type_id: str
    reason: str | None = None
    rule: str | None = None
    is_rollable: bool | None = None
    roll_date: datetime | None = None
    is_held: bool | None = None
    release_date: datetime | None = None
    pipeline_run: str | None = None
    pipeline_run_date: datetime | None = None
    compensation_date: datetime | None = None
    comments: str | None = None
    is_private: bool | None = None
    business_units: list[str] | None = None
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
    gd1: datetime | None = pydantic.Field(None, alias="generic_date1")
    gd2: datetime | None = pydantic.Field(None, alias="generic_date2")
    gd3: datetime | None = pydantic.Field(None, alias="generic_date3")
    gd4: datetime | None = pydantic.Field(None, alias="generic_date4")
    gd5: datetime | None = pydantic.Field(None, alias="generic_date5")
    gd6: datetime | None = pydantic.Field(None, alias="generic_date6")
    gb1: bool | None = pydantic.Field(None, alias="genericBoolean1")
    gb2: bool | None = pydantic.Field(None, alias="genericBoolean2")
    gb3: bool | None = pydantic.Field(None, alias="genericBoolean3")
    gb4: bool | None = pydantic.Field(None, alias="genericBoolean4")
    gb5: bool | None = pydantic.Field(None, alias="genericBoolean5")
    gb6: bool | None = pydantic.Field(None, alias="genericBoolean6")
    processing_unit: str = pydantic.Field(repr=False)


class CreditType(_DataType):
    """Credit Type."""

    _endpoint: ClassVar[str] = "api/v2/creditTypes"
    credit_type_id: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("credit_type_id", "ID", "Credit Type ID")
    )


class EarningCode(_DataType):
    """Earning Code."""

    _endpoint: ClassVar[str] = "api/v2/earningCodes"
    earning_code_id: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("earningCodeId", "ID")
    )


class EarningGroup(_DataType):
    """Earning Group."""

    _endpoint: ClassVar[str] = "api/v2/earningGroups"
    earning_group_id: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("earningGroupId", "ID")
    )


class EventType(_DataType):
    """Class representation of an Event Type."""

    _endpoint: ClassVar[str] = "api/v2/eventTypes"
    event_type_id: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("event_type_id", "ID"),
    )


class FixedValueType(_DataType):
    """Fixed Value Type."""

    _endpoint: ClassVar[str] = "api/v2/fixedValueTypes"
    fixed_value_type_id: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("fixedValue_type_id", "ID")
    )


class Period(_Resource):
    """Period."""

    _endpoint: ClassVar[str] = "api/v2/periods"
    _attr_seq: ClassVar[str] = "period_seq"
    period_seq: str | None = None
    name: str
    short_name: str
    start_date: datetime
    end_date: datetime
    period_type: str
    calendar: str
    description: str | None = None
    parent: str | None = None


class PeriodType(_Resource):
    """Period Type."""

    _endpoint: ClassVar[str] = "api/v2/periodTypes"
    _attr_seq: ClassVar[str] = "period_type_seq"
    period_type_seq: str | None = None
    name: str
    description: str | None = None
    level: int | None = None


class Pipeline(_Resource):
    """Pipeline."""

    _endpoint: ClassVar[str] = "api/v2/pipelines"
    _attr_seq: ClassVar[str] = "pipeline_run_seq"
    pipeline_run_seq: str | None = None
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
    stage_type: (
        const.PipelineRunStages
        | const.ImportStages
        | const.XMLImportStages
        | const.MaintenanceStages
        | None
    )
    date_submitted: datetime
    state: const.PipelineState
    user_id: str
    processing_unit: str = pydantic.Field(repr=False)
    period: str | None = None
    description: str | None = None
    status: const.PipelineStatus | None = None
    run_progress: float | None = None
    start_time: datetime | None = pydantic.Field(None, repr=False)
    stop_time: datetime | None = pydantic.Field(None, repr=False)
    start_date_scheduled: datetime | None = pydantic.Field(None, repr=False)
    batch_name: str | None = None
    priority: int | None = pydantic.Field(repr=False)
    message: str | None = pydantic.Field(None, repr=False)
    num_errors: int | None = pydantic.Field(repr=False)
    num_warnings: int | None = pydantic.Field(repr=False)
    run_mode: const.ImportRunMode | const.PipelineRunMode | None = pydantic.Field(
        None, repr=False
    )

    @pydantic.field_validator("run_progress", mode="before")
    @classmethod
    def percent_as_float(cls, value: str) -> float | None:
        """Convert percentage string to float."""
        return int(value.removesuffix("%")) / 100 if value else None


class Position(_RuleElementOwner):
    """Position."""

    _endpoint: ClassVar[str] = "api/v2/positions"
    name: str
    description: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    credit_start_date: datetime | None = None
    credit_end_date: datetime | None = None
    processing_start_date: datetime | None = None
    processing_end_date: datetime | None = None
    target_compensation: dict | None = None
    processing_unit: str | None = None
    business_units: list[str] | None = None
    manager: str | None = None
    title: str | None = None
    plan: str | None = None
    position_group: str | None = None
    payee: str | None = None
    variable_assignments: Assignment | list[Assignment] | None = None
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
    gd1: datetime | None = pydantic.Field(None, alias="generic_date1")
    gd2: datetime | None = pydantic.Field(None, alias="generic_date2")
    gd3: datetime | None = pydantic.Field(None, alias="generic_date3")
    gd4: datetime | None = pydantic.Field(None, alias="generic_date4")
    gd5: datetime | None = pydantic.Field(None, alias="generic_date5")
    gd6: datetime | None = pydantic.Field(None, alias="generic_date6")
    gb1: bool | None = pydantic.Field(None, alias="genericBoolean1")
    gb2: bool | None = pydantic.Field(None, alias="genericBoolean2")
    gb3: bool | None = pydantic.Field(None, alias="genericBoolean3")
    gb4: bool | None = pydantic.Field(None, alias="genericBoolean4")
    gb5: bool | None = pydantic.Field(None, alias="genericBoolean5")
    gb6: bool | None = pydantic.Field(None, alias="genericBoolean6")


class PositionGroup(_Resource):
    """Position."""

    _endpoint: ClassVar[str] = "api/v2/positionGroups"
    _attr_seq: ClassVar[str] = "position_group_seq"
    position_group_seq: str | None = None
    name: str
    business_units: list[str] | None = None


class ProcessingUnit(_Resource):
    """Processing Unit."""

    _endpoint: ClassVar[str] = "api/v2/processingUnits"
    _attr_seq: ClassVar[str] = "processing_unit_seq"
    processing_unit_seq: str | None = None
    name: str
    description: str | None = None


class ReasonCode(_DataType):
    """Reason Code."""

    _endpoint: ClassVar[str] = "api/v2/reasons"
    reason_id: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("reasonId", "ID")
    )


class Title(_RuleElementOwner):
    """Title."""

    _endpoint: ClassVar[str] = "api/v2/titles"
    name: str
    description: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    plan: str | None = None
    variable_assignments: Assignment | list[Assignment | str] | None = None
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
    gd1: datetime | None = pydantic.Field(None, alias="generic_date1")
    gd2: datetime | None = pydantic.Field(None, alias="generic_date2")
    gd3: datetime | None = pydantic.Field(None, alias="generic_date3")
    gd4: datetime | None = pydantic.Field(None, alias="generic_date4")
    gd5: datetime | None = pydantic.Field(None, alias="generic_date5")
    gd6: datetime | None = pydantic.Field(None, alias="generic_date6")
    gb1: bool | None = pydantic.Field(None, alias="genericBoolean1")
    gb2: bool | None = pydantic.Field(None, alias="genericBoolean2")
    gb3: bool | None = pydantic.Field(None, alias="genericBoolean3")
    gb4: bool | None = pydantic.Field(None, alias="genericBoolean4")
    gb5: bool | None = pydantic.Field(None, alias="genericBoolean5")
    gb6: bool | None = pydantic.Field(None, alias="genericBoolean6")


class _PipelineJob(_Endpoint):
    """Base class for a Pipeline Job."""

    _endpoint: ClassVar[str] = "api/v2/pipelines"
    command: Literal["PipelineRun", "Import", "XMLImport"]
    run_stats: bool = False


class ResetFromValidate(_PipelineJob):
    """Run a ResetFromValidate pipeline."""

    _endpoint: ClassVar[str] = "api/v2/pipelines/resetfromvalidate"
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

    @pydantic.computed_field
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

    @pydantic.model_validator(mode="after")
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
    generate_ods_reports: Literal[True] = True
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

    @pydantic.computed_field
    def stage_tables(self) -> list[str]:
        """Compute stageTables field based on module."""
        return STAGETABLES[self.module]

    @pydantic.model_validator(mode="after")
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
