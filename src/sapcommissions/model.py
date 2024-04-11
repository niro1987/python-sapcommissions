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
        protected_namespaces=(
            "model_computed_fields",
            "model_config",
            "model_construct",
            "model_copy",
            "model_dump",
            "model_dump_json",
            "model_extra",
            "model_fields",
            "model_fields_set",
            "model_json_schema",
            "model_parametrized_name",
            "model_post_init",
            "model_rebuild",
            "model_validate",
            "model_validate_json",
            "model_validate_strings",
        ),
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

    value: int | float | None
    unit_type: ValueUnitType


class RuleUsage(_BaseModel):
    """BaseModel for RuleUsage."""

    id: str
    name: str


class RuleUsageList(_BaseModel):
    """BaseModel for RuleUsage lists."""

    children: list[RuleUsage]


class BusinessUnitAssignment(_BaseModel):
    """BaseModel for BusinessUnitAssignment."""

    mask: int
    smask: int


class Generic16Mixin(_BaseModel):
    """Mixin to add Generic Attributes to a model."""

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


class Generic32Mixin(Generic16Mixin):
    """Mixin to add extended Generic Attributes to a model."""

    ga17: str | None = pydantic.Field(None, alias="genericAttribute17")
    ga18: str | None = pydantic.Field(None, alias="genericAttribute18")
    ga19: str | None = pydantic.Field(None, alias="genericAttribute19")
    ga20: str | None = pydantic.Field(None, alias="genericAttribute20")
    ga21: str | None = pydantic.Field(None, alias="genericAttribute21")
    ga22: str | None = pydantic.Field(None, alias="genericAttribute22")
    ga23: str | None = pydantic.Field(None, alias="genericAttribute23")
    ga24: str | None = pydantic.Field(None, alias="genericAttribute24")
    ga25: str | None = pydantic.Field(None, alias="genericAttribute25")
    ga26: str | None = pydantic.Field(None, alias="genericAttribute26")
    ga27: str | None = pydantic.Field(None, alias="genericAttribute27")
    ga28: str | None = pydantic.Field(None, alias="genericAttribute28")
    ga29: str | None = pydantic.Field(None, alias="genericAttribute29")
    ga30: str | None = pydantic.Field(None, alias="genericAttribute30")
    ga31: str | None = pydantic.Field(None, alias="genericAttribute31")
    ga32: str | None = pydantic.Field(None, alias="genericAttribute32")


class AdjustmentContext(_BaseModel):
    """Adjustment Context for a Sales Transaction."""

    adjust_type_flag: Literal["adjustTo", "adjustBy", "reset"]
    adjust_to_value: Value | None = None
    adjust_by_value: Value | None = None
    comment: str | None = None


class _Endpoint(_BaseModel):
    """BaseModel for an Endpoint."""

    attr_endpoint: ClassVar[str]


class _Resource(_Endpoint):
    """Base class for a Resource."""

    _attr_seq: ClassVar[str]
    _expand: ClassVar[list[str]] = []
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

    @classmethod
    def get_expand(cls) -> list[str]:
        """Return the expand attribute for the resource."""
        expands: list[str] = []
        for field in cls._expand:
            if not (field_info := cls.model_fields.get(field)):
                raise ValueError(f"'{field}' not found in {cls.__name__}")
            if not (field_alias := field_info.alias):
                raise ValueError(f"'{field}' has no alias in {cls.__name__}")
            expands.append(field_alias)
        return expands


class _DataType(_Resource):
    """Base class for Data Type resources."""

    _attr_seq: ClassVar[str] = "data_type_seq"
    data_type_seq: str | None = None
    description: str | None = pydantic.Field(
        None,
        validation_alias=pydantic.AliasChoices("description", "Description"),
    )
    not_allow_update: bool | None = None


class _RuleElement(_Resource):
    """Base class for Rule Element resources."""

    _attr_seq: ClassVar[str] = "rule_element_seq"
    rule_element_seq: str | None = None
    name: str
    description: str | None = None


class _RuleElementOwner(_Resource):
    """Base class for Rule Element Owner resources."""

    _attr_seq: ClassVar[str] = "rule_element_owner_seq"
    rule_element_owner_seq: str | None = None
    name: str
    description: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime


class AppliedDeposit(_Resource):
    """AppliedDeposit."""

    attr_endpoint: ClassVar[str] = "api/v2/appliedDeposits"
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


class AuditLog(_Resource):
    """Audit Log."""

    attr_endpoint: ClassVar[str] = "api/v2/auditLogs"
    _attr_seq: ClassVar[str] = "audit_log_seq"
    audit_log_seq: str | None = None
    event_date: datetime
    event_type: str
    event_description: str | None = None
    business_unit: BusinessUnitAssignment
    object_seq: str
    object_name: str
    object_type: str
    user_id: str
    model_seq: str | None = None


class Balance(_Resource):
    """Balance."""

    attr_endpoint: ClassVar[str] = "api/v2/balances"
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

    attr_endpoint: ClassVar[str] = "api/v2/businessUnits"
    _attr_seq: ClassVar[str] = "business_unit_seq"
    business_unit_seq: str | None = None
    name: str
    description: str | None = None
    mask: str | None = None
    processing_unit: str | None = None


class Calendar(_Resource):
    """Calendar."""

    attr_endpoint: ClassVar[str] = "api/v2/calendars"
    calendar_seq: str | None = None
    name: str
    description: str | None = None
    minor_period_type: str | None = None
    major_period_type: str | None = None
    periods: list[str] | None = None


class Category(_RuleElement, Generic16Mixin):
    """Category."""

    attr_endpoint: ClassVar[str] = "api/v2/categories"
    owner: str
    parent: str | None = None
    return_type: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    rule_usage: RuleUsageList | None = None
    owning_element: str | None = None
    calendar: str | None = None
    input_signature: str | None = None
    not_allow_update: bool = False
    model_seq: str | None = None


class CategoryClassifier(_Resource):
    """categoryClassifier."""

    attr_endpoint: ClassVar[str] = "api/v2/categoryClassifiers"
    _attr_seq: ClassVar[str] = "category_classifiers_seq"
    category_classifiers_seq: str | None = None
    category_tree: str
    category: str
    classifier: str
    effective_start_date: datetime
    effective_end_date: datetime


class CategoryTree(_Resource):
    """CategoryTree."""

    attr_endpoint: ClassVar[str] = "api/v2/categoryTrees"
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

    attr_endpoint: ClassVar[str] = "api/v2/commissions"
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


class Credit(_Resource, Generic16Mixin):
    """Credit."""

    attr_endpoint: ClassVar[str] = "api/v2/credits"
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
    processing_unit: str = pydantic.Field(repr=False)


class CreditType(_DataType):
    """Credit Type."""

    attr_endpoint: ClassVar[str] = "api/v2/creditTypes"
    credit_type_id: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("creditTypeId", "ID", "Credit Type ID")
    )


class Deposit(_Resource, Generic16Mixin):
    """Deposit."""

    attr_endpoint: ClassVar[str] = "api/v2/deposits"
    _attr_seq: ClassVar[str] = "deposit_seq"
    deposit_seq: str | None = None
    name: str
    earning_group_id: str
    earning_code_id: str
    payee: str
    position: str
    period: str
    value: Value
    preadjusted_value: Value
    origin_type_id: str
    reason: str | None = None
    businessUnits: list[str] | None = None
    rule: str | None = None
    deposit_date: datetime | None = None
    is_held: bool | None = None
    release_date: datetime | None = None
    pipeline_run: str | None = None
    pipeline_run_date: datetime | None = None
    processing_unit: str | None = None
    comments: str | None = None
    is_private: bool | None = None
    model_seq: str | None = None


class EarningCode(_DataType):
    """Earning Code."""

    attr_endpoint: ClassVar[str] = "api/v2/earningCodes"
    earning_code_id: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("earningCodeId", "ID")
    )


class EarningGroup(_DataType):
    """Earning Group."""

    attr_endpoint: ClassVar[str] = "api/v2/earningGroups"
    earning_group_id: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("earningGroupId", "ID")
    )


class EarningGroupCode(_Resource):
    """EarningGroupCode."""

    attr_endpoint: ClassVar[str] = "api/v2/earningGroupCodes"
    _attr_seq: ClassVar[str] = "earning_group_code_seq"
    earning_group_code_seq: str | None = None
    earning_group_code: str
    earning_code_id: str
    earning_group_id: str


class EventType(_DataType):
    """Class representation of an Event Type."""

    attr_endpoint: ClassVar[str] = "api/v2/eventTypes"
    event_type_id: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("eventTypeId", "ID"),
    )


class FixedValue(_RuleElementOwner):
    """Fixed Value."""

    attr_endpoint: ClassVar[str] = "api/v2/fixedValues"
    calendar: str
    value: Value | None = None
    fixedValueType: str | None = None
    business_units: list[str] | None = None
    periodType: str | None = None
    owning_element: str | None = None
    rule_usage: RuleUsageList | None = None
    rule_element_seq: str | None = None
    not_allow_update: bool = False
    model_seq: str | None = None
    input_signature: str | None = None
    return_type: str | None = None


class FixedValueType(_DataType):
    """Fixed Value Type."""

    attr_endpoint: ClassVar[str] = "api/v2/fixedValueTypes"
    fixed_value_type_id: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("fixedValueTypeId", "ID")
    )


class FixedValueVariable(_RuleElement):
    """Fixed Value Variable."""

    attr_endpoint: ClassVar[str] = "api/v2/fixedValueVariables"
    calendar: str
    effective_start_date: datetime
    effective_end_date: datetime
    required_period_type: str | None = None
    business_units: list[str] | None = None
    not_allow_update: bool = False
    default_element: str | None = None
    model_seq: str | None = None
    reference_class_type: str | None = None
    return_type: str | None = None
    owning_element: str | None = None
    rule_usage: RuleUsageList | None = None
    input_signature: str | None = None


class GenericClassifier(_Resource, Generic16Mixin):
    """Generic Classifier."""

    attr_endpoint: ClassVar[str] = "api/v2/genericClassifiers"
    _attr_seq: ClassVar[str] = "generic_classifier_seq"
    generic_classifier_seq: str | None = None
    name: str | None = None
    description: str | None = None
    classifier_id: str
    classifier_seq: str
    selector_id: str
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None


class GenericClassifierType(_Resource):
    """Generic Classifier Type."""

    attr_endpoint: ClassVar[str] = "api/v2/genericClassifierTypes"
    _attr_seq: ClassVar[str] = "generic_classifier_type_seq"
    generic_classifier_type_seq: int | None = None
    name: str


class GlobalFieldName(_Resource):
    """Global Field Name."""

    attr_endpoint: ClassVar[str] = "api/v2/globalFieldNames"
    _attr_seq: ClassVar[str] = "global_field_name_seq"
    global_field_name_seq: str | None = None
    name: str
    description: str | None = None
    global_field_name_data_type_length: int


# class Group(_Resource):
#     """Group."""

#     attr_endpoint: ClassVar[str] = "api/v2/groups"
#     _attr_seq: ClassVar[str] = "group_seq"
#     group_seq: str | None = None
#     name: str
#     description: str | None = None


class Incentive(_Resource, Generic16Mixin):
    """Incentive."""

    attr_endpoint: ClassVar[str] = "api/v2/incentives"
    _attr_seq: ClassVar[str] = "incentive_seq"
    incentive_seq: str | None = None
    name: str | None = None
    quota: Value | None = None
    attainment: Value | None = None
    position: str
    payee: str
    period: str
    rule: str
    value: Value
    release_date: datetime | None = None
    pipeline_run: str | None = None
    pipeline_run_date: datetime | None = None
    is_active: bool = True
    is_private: bool | None = None
    processing_unit: str | None = None
    business_units: list[str] | None = None


class LookUpTableVariable(_RuleElement):
    """LookUp Table Variable."""

    attr_endpoint: ClassVar[str] = "api/v2/lookUpTableVariables"
    calendar: str
    default_element: str | None = None
    required_period_type: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    not_allow_update: bool = False
    model_seq: str | None = None
    reference_class_type: str | None = None
    return_type: str | None = None
    owning_element: str | None = None
    input_signature: str | None = None
    rule_usage: RuleUsageList | None = None


class Measurement(_Resource, Generic16Mixin):
    """Measurement."""

    attr_endpoint: ClassVar[str] = "api/v2/measurements"
    _attr_seq: ClassVar[str] = "measurement_seq"
    measurement_seq: str | None = None
    name: str
    position: str
    payee: str
    period: str
    rule: str | None = None
    value: Value
    pipeline_run: str | None = None
    pipeline_run_date: datetime | None = None
    number_of_credits: Value
    is_private: bool | None = None
    processing_unit: str | None = None
    business_units: list[str] | None = None


class PrimaryMeasurement(Measurement):
    """Primary Measurement."""

    attr_endpoint: ClassVar[str] = "api/v2/primaryMeasurements"


class SecondaryMeasurement(Measurement):
    """Secondary Measurement."""

    attr_endpoint: ClassVar[str] = "api/v2/secondaryMeasurements"


class Message(_Resource):
    """Message."""

    attr_endpoint: ClassVar[str] = "api/v2/messages"
    _attr_seq: ClassVar[str] = "message_seq"
    message_seq: str | None = None
    message_key: str
    message_time_stamp: datetime
    argument_count: int
    sub_category: str
    message_log: str
    module: str
    rule: str | None = None
    payee: str | None = None
    message_type: str
    run_period: str | None = None
    object_seq: str | None = None
    sales_transaction: str | None = None
    position: str | None = None
    category: str | None = None
    credit: str | None = None


class MessageLog(_Resource):
    """Message Log."""

    attr_endpoint: ClassVar[str] = "api/v2/messageLogs"
    _attr_seq: ClassVar[str] = "message_log_seq"
    message_log_seq: str | None = None
    source_seq: str | None = None
    component_name: str
    log_date: datetime
    log_name: str


class Participant(_Resource, Generic16Mixin):
    """Participant."""

    attr_endpoint: ClassVar[str] = "api/v2/participants"
    _attr_seq: ClassVar[str] = "payee_seq"
    payee_seq: str | None = None
    payee_id: str
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str
    participant_email: str | None = None
    prefix: str | None = None
    suffix: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    hire_date: datetime | None = None
    termination_date: datetime | None = None
    salary: Value | None = None
    user_id: str
    preferred_language: str | None = None
    event_calendar: str | None = None
    tax_id: str | None = None
    business_units: list[str] | None = None


# class Payment(_Resource):
#     """Payment."""

#     attr_endpoint: ClassVar[str] = "api/v2/payments"
#     _attr_seq: ClassVar[str] = "payment_seq"
#     payment_seq: str | None = None
#     position: str
#     payee: str
#     period: str
#     earning_group_id: str
#     earning_code_id: str
#     trial_pipeline_run: str | None = None
#     trial_pipeline_run_date: datetime | None = None
#     post_pipeline_run: str | None = None
#     post_pipeline_run_date: datetime | None = None
#     reason: str | None = None
#     value: Value
#     processingUnit: str | None = None


class PaymentMapping(_Resource):
    """Payment Mapping."""

    attr_endpoint: ClassVar[str] = "api/v2/paymentMappings"
    _attr_seq: ClassVar[str] = "payment_mapping_seq"
    payment_mapping_seq: str | None = None
    source_table_name: str
    source_attribute: str
    payment_attribute: str


class PaymentSummary(_Resource):
    """Payment Summary."""

    attr_endpoint: ClassVar[str] = "api/v2/paymentSummarys"
    _attr_seq: ClassVar[str] = "payment_summary_seq"
    payment_summary_seq: str | None = None
    position: str
    participant: str
    period: str
    earning_group_id: str
    pipeline_run: str | None = None
    pipeline_run_date: datetime | None = None
    applied_deposit: Value | None = None
    balance: Value | None = None
    prior_balance: Value | None = None
    outstanding_balance: Value | None = None
    payment: Value | None = None
    business_units: list[str] | None = None
    processingUnit: str | None = None


class Period(_Resource):
    """Period."""

    attr_endpoint: ClassVar[str] = "api/v2/periods"
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

    attr_endpoint: ClassVar[str] = "api/v2/periodTypes"
    _attr_seq: ClassVar[str] = "period_type_seq"
    period_type_seq: str | None = None
    name: str
    description: str | None = None
    level: int | None = None


class Pipeline(_Resource):
    """Pipeline."""

    attr_endpoint: ClassVar[str] = "api/v2/pipelines"
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
    start_time: datetime | None = None
    stop_time: datetime | None = None
    start_date_scheduled: datetime | None = None
    batch_name: str | None = None
    priority: int | None = pydantic.Field(repr=False)
    message: str | None = None
    num_errors: int | None = pydantic.Field(repr=False)
    num_warnings: int | None = pydantic.Field(repr=False)
    run_mode: const.ImportRunMode | const.PipelineRunMode | None = pydantic.Field(
        None, repr=False
    )
    product_version: str | None = None
    stored_proc_version: str | None = None
    schema_version: str | None = None
    remove_date: datetime | None = None
    end_date_scheduled: datetime | None = None
    run_parameters: str | None = None
    trace_level: str | None = None
    report_type_name: str | None = None
    target_database: str | None = None
    schedule_frequency: str | None = None
    group_name: str | None = None
    isolation_level: str | None = None
    schedule_day: str | None = None
    stage_tables: list[Assignment] | Assignment | None = pydantic.Field(
        None, repr=False
    )
    model_seq: str | None = None
    model_run: str | None = None

    @pydantic.field_validator("run_progress", mode="before")
    @classmethod
    def percent_as_float(cls, value: str) -> float | None:
        """Convert percentage string to float."""
        return int(value.removesuffix("%")) / 100 if value else None


class Position(_RuleElementOwner, Generic16Mixin):
    """Position."""

    attr_endpoint: ClassVar[str] = "api/v2/positions"
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
    variable_assignments: list[Assignment] | Assignment | None = None
    model_seq: str | None = None


class PositionGroup(_Resource):
    """Position."""

    attr_endpoint: ClassVar[str] = "api/v2/positionGroups"
    _attr_seq: ClassVar[str] = "position_group_seq"
    position_group_seq: str | None = None
    name: str
    business_units: list[str] | None = None


class PositionRelation(_Resource):
    """Position Relation."""

    attr_endpoint: ClassVar[str] = "api/v2/positionRelations"
    _attr_seq: ClassVar[str] = "position_relation_seq"
    position_relation_seq: str | None = None
    name: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    parent_position: str
    position_relation_type: str
    child_position: str


class PositionRelationType(_DataType):
    """Position Relation Type."""

    attr_endpoint: ClassVar[str] = "api/v2/positionRelationTypes"
    name: str


class PostalCode(_Resource, Generic16Mixin):
    """Postal Code."""

    attr_endpoint: ClassVar[str] = "api/v2/postalCodes"
    _attr_seq: ClassVar[str] = "classifier_seq"
    classifier_seq: str | None = None
    classifier_id: str
    low_postal_code: str
    high_postal_code: str
    country: str
    name: str | None = None
    description: str | None = None
    selector_id: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None


class ProcessingUnit(_Resource):
    """Processing Unit."""

    attr_endpoint: ClassVar[str] = "api/v2/processingUnits"
    _attr_seq: ClassVar[str] = "processing_unit_seq"
    processing_unit_seq: str | None = None
    name: str
    description: str | None = None


class Product(_Resource, Generic16Mixin):
    """Product."""

    attr_endpoint: ClassVar[str] = "api/v2/products"
    _attr_seq: ClassVar[str] = "classifier_seq"
    classifier_seq: str | None = None
    classifier_id: str
    name: str | None = None
    cost: Value | None = None
    price: Value | None = None
    description: str | None = None
    selector_id: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None


class Quota(_Resource):
    """Quota."""

    attr_endpoint: ClassVar[str] = "api/v2/quotas"
    _attr_seq: ClassVar[str] = "quota_seq"
    quota_seq: str | None = None
    calendar: str
    name: str
    description: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    unit_type: str
    model_seq: str | None = None
    business_units: list[str] | None = None


class RateTableVariable(_RuleElement):
    """Rate Table Variable."""

    attr_endpoint: ClassVar[str] = "api/v2/rateTableVariables"
    calendar: str
    default_element: str | None = None
    required_period_type: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    not_allow_update: bool = False
    model_seq: str | None = None
    reference_class_type: str | None = None
    return_type: str | None = None
    owning_element: str | None = None
    rule_usage: RuleUsageList | None = None
    input_signature: str | None = None


class Reason(_DataType):
    """Reason."""

    attr_endpoint: ClassVar[str] = "api/v2/reasons"
    reason_id: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices("reasonId", "ID")
    )


class SalesOrder(_Resource, Generic16Mixin):
    """Sales Order."""

    attr_endpoint: ClassVar[str] = "api/v2/salesOrders"
    _attr_seq: ClassVar[str] = "sales_order_seq"
    sales_order_seq: str | None = None
    order_id: str
    pipeline_run: str | None = None
    business_units: list[str] | None = None
    processing_unit: str | None = None
    model_seq: str | None = None


class SalesTransaction(_Resource, Generic32Mixin):
    """Sales Transaction."""

    attr_endpoint: ClassVar[str] = "api/v2/salesTransactions"
    _attr_seq: ClassVar[str] = "sales_transaction_seq"
    sales_transaction_seq: str | None = None
    sales_order: str
    line_number: Value
    sub_line_number: Value
    event_type: str
    product_id: str | None = None
    product_name: str | None = None
    product_description: str | None = None
    value: Value
    preadjusted_value: Value | None = None
    is_runnable: bool | None = None
    compensation_date: datetime
    number_of_units: Value | None = None
    unit_value: Value | None = None
    business_units: list[str] | None = None
    processing_unit: str | None = None
    model_seq: str | None = None
    ship_to_address: str | None = None
    bill_to_address: str | None = None
    other_to_address: str | None = None
    transaction_assignments: list[Assignment] | Assignment | None = None
    payment_terms: str | None = None
    accounting_date: datetime | None = None
    discount_percent: Value | None = None
    comments: str | None = None
    native_currency_amount: Value | None = None
    native_currency: str | None = None
    pipeline_run: str | None = None
    alternate_order_number: str | None = None
    origin_type_id: str | None = None
    adjustment_context: AdjustmentContext | None = None
    is_purged: bool | None = None
    reason: str | None = None
    channel: str | None = None
    po_number: str | None = None
    data_source: str | None = None
    discount_type: str | None = None
    modification_date: datetime | None = None


class StatusCode(_DataType):
    """Status Code."""

    attr_endpoint: ClassVar[str] = "api/v2/statusCodes"
    name: str | None = None
    type: str | None = None
    status: str
    is_active: bool = True


class Territory(_RuleElement):
    """Territory."""

    attr_endpoint: ClassVar[str] = "api/v2/territories"
    calendar: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    not_allow_update: bool = False
    model_seq: str | None = None
    return_type: str | None = None
    rule_usage: RuleUsage | RuleUsageList | None = None
    owning_element: str | None = None
    input_signature: str | None = None


class TerritoryVariable(_RuleElement):
    """Territory Variable."""

    attr_endpoint: ClassVar[str] = "api/v2/territoryVariables"
    calendar: str
    effective_start_date: datetime
    effective_end_date: datetime
    required_period_type: str | None = None
    business_units: list[str] | None = None
    not_allow_update: bool = False
    default_element: str | None = None
    model_seq: str | None = None
    reference_class_type: str | None = None
    return_type: str | None = None
    owning_element: str | None = None
    rule_usage: RuleUsageList | None = None
    input_signature: str | None = None


class Title(_RuleElementOwner, Generic16Mixin):
    """Title."""

    attr_endpoint: ClassVar[str] = "api/v2/titles"
    business_units: list[str] | None = None
    plan: str | None = None
    variable_assignments: list[Assignment] | Assignment | None = None
    model_seq: str | None = None


class User(_Resource):
    """User."""

    attr_endpoint: ClassVar[str] = "api/v2/users"
    _attr_seq: ClassVar[str] = "user_seq"
    user_seq: str | None = None
    id: str
    user_name: str | None = None
    description: str | None = None
    email: str | None = None
    read_only_business_unit_list: list[dict[Literal["name"], str]] | None = None
    full_access_business_unit_list: list[dict[Literal["name"], str]] | None = None
    preferred_language: str | None = None
    last_login: datetime | None = None


class Variable(_RuleElement):
    """Variable."""

    attr_endpoint: ClassVar[str] = "api/v2/variables"
    calendar: str
    effective_start_date: datetime
    effective_end_date: datetime
    required_period_type: str | None = None
    business_units: list[str] | None = None
    not_allow_update: bool = False
    default_element: str | None = None
    model_seq: str | None = None
    reference_class_type: str | None = None
    return_type: str | None = None
    owning_element: str | None = None
    rule_usage: RuleUsageList | None = None
    input_signature: str | None = None


class RelationalMDLT(_RuleElement):
    """Relational MDLT."""

    attr_endpoint: ClassVar[str] = "api/v2/relationalMDLTs"
    calendar: str
    effective_start_date: datetime
    effective_end_date: datetime
    required_period_type: str | None = None
    business_units: list[str] | None = None
    not_allow_update: bool = False
    default_element: str | None = None
    model_seq: str | None = None
    reference_class_type: str | None = None
    return_type: str | None = None
    owning_element: str | None = None
    rule_usage: RuleUsageList | None = None
    input_signature: str | None = None
    return_unit_type: str | None = None
    indices: list[Assignment] | Assignment | None = None
    treat_null_as_zero: bool | None = None
    expression_type_counts: str | None = None
    dimensions: list[Assignment] | Assignment | None = None


class RateTable(_RuleElement):
    """Rate Table."""

    attr_endpoint: ClassVar[str] = "api/v2/rateTables"
    calendar: str
    effective_start_date: datetime
    effective_end_date: datetime
    required_period_type: str | None = None
    business_units: list[str] | None = None
    not_allow_update: bool = False
    default_element: str | None = None
    model_seq: str | None = None
    reference_class_type: str | None = None
    return_type: str | None = None
    owning_element: str | None = None
    rule_usage: RuleUsageList | None = None
    input_signature: str | None = None
    return_unit_type: str | None = None


class Formula(_RuleElement):
    """Formula."""

    attr_endpoint: ClassVar[str] = "api/v2/formulas"
    calendar: str
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    not_allow_update: bool = False
    model_seq: str | None = None
    return_type: str | None = None
    owning_element: str | None = None
    rule_usage: RuleUsageList | RuleUsage | None = None
    input_signature: str | None = None


class Plan(_RuleElementOwner):
    """Plan."""

    attr_endpoint: ClassVar[str] = "api/v2/plans"
    calendar: str
    business_units: list[str] | None = None
    variable_assignments: list[Assignment] | Assignment | None = None
    model_seq: str | None = None


class PlanComponent(_Resource):
    """Plan."""

    attr_endpoint: ClassVar[str] = "api/v2/planComponents"
    _attr_seq: ClassVar[str] = "plan_component_seq"
    plan_component_seq: str | None = None
    name: str
    description: str | None = None
    calendar: str
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    not_allow_update: bool = False
    model_seq: str | None = None


class Rule(_Resource):
    """Rule."""

    attr_endpoint: ClassVar[str] = "api/v2/rules"
    _attr_seq: ClassVar[str] = "rule_seq"
    rule_seq: str | None = None
    name: str
    description: str | None = None
    calendar: str
    effective_start_date: datetime
    effective_end_date: datetime
    business_unit: list[BusinessUnitAssignment] | BusinessUnitAssignment | None = None
    type: RuleUsage | None = None
    not_allow_update: bool = False
    model_seq: str | None = None


class _PipelineJob(_Endpoint):
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
