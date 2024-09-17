"""Resource models for Python SAP Commissions Client."""

from datetime import datetime
from typing import ClassVar, Literal

from pydantic import Field, field_validator

from sapcommissions import const

from .base import (
    AdjustmentContext,
    Assignment,
    BusinessUnitAssignment,
    Generic16Mixin,
    Generic32Mixin,
    Reference,
    Resource,
    RuleUsage,
    Value,
)


class AppliedDeposit(Resource):
    """AppliedDeposit."""

    attr_endpoint: ClassVar[str] = "api/v2/appliedDeposits"
    attr_seq: ClassVar[str] = "applied_deposit_seq"
    applied_deposit_seq: str | None = None
    position: str | Reference
    payee: str | Reference
    period: str | Reference
    earning_group_id: str
    earning_code_id: str
    trial_pipeline_run: str
    trial_pipeline_run_date: datetime
    post_pipeline_run: str | None = None
    post_pipeline_run_date: datetime | None = None
    entry_number: str
    value: Value
    processing_unit: str | None = None


class AuditLog(Resource):
    """Audit Log."""

    attr_endpoint: ClassVar[str] = "api/v2/auditLogs"
    attr_seq: ClassVar[str] = "audit_log_seq"
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


class Balance(Resource):
    """Balance."""

    attr_endpoint: ClassVar[str] = "api/v2/balances"
    attr_seq: ClassVar[str] = "balance_seq"
    balance_seq: str | None = None
    position: str | Reference
    payee: str | Reference
    period: str | Reference
    earning_group_id: str
    earning_code_id: str
    trial_pipeline_run: str
    trial_pipeline_run_date: datetime
    apply_pipeline_run: str | None = None
    apply_pipeline_run_date: datetime | None = None
    post_pipeline_run: str | None = None
    post_pipeline_run_date: datetime | None = None
    balance_status_id: str
    value: Value
    processing_unit: str | None = None


class BusinessUnit(Resource):
    """Business Unit."""

    attr_endpoint: ClassVar[str] = "api/v2/businessUnits"
    attr_seq: ClassVar[str] = "business_unit_seq"
    business_unit_seq: str | None = None
    name: str
    description: str | None = None
    mask: str | None = None
    processing_unit: str | None = None


class Calendar(Resource):
    """Calendar."""

    attr_endpoint: ClassVar[str] = "api/v2/calendars"
    attr_seq: ClassVar[str] = "calendar_seq"
    calendar_seq: str | None = None
    name: str
    description: str | None = None
    minor_period_type: str | Reference | Reference | None = None
    major_period_type: str | Reference | Reference | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class CategoryClassifier(Resource):
    """categoryClassifier."""

    attr_endpoint: ClassVar[str] = "api/v2/categoryClassifiers"
    attr_seq: ClassVar[str] = "category_classifiers_seq"
    category_classifiers_seq: str | None = None
    category_tree: str | Reference
    category: str | Reference
    classifier: str | Reference
    effective_start_date: datetime
    effective_end_date: datetime
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class CategoryTree(Resource):
    """CategoryTree."""

    attr_endpoint: ClassVar[str] = "api/v2/categoryTrees"
    attr_seq: ClassVar[str] = "category_tree_seq"
    category_tree_seq: str | None = None
    name: str
    description: str | None = None
    classifier_selector_id: str | None = None
    classifier_class: str
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class Commission(Resource):
    """Commission.

    TODO: No results.
    """

    attr_endpoint: ClassVar[str] = "api/v2/commissions"
    attr_seq: ClassVar[str] = "commission_seq"
    commission_seq: str | None = None
    position: str | Reference
    payee: str | Reference
    period: str | Reference
    incentive: str | Reference
    credit: str | Reference
    pipeline_run: str
    pipeline_run_date: datetime
    value: Value
    rate_value: Value
    entry_number: Value
    business_units: list[str] | None = None
    processing_unit: str = Field(repr=False)
    is_private: bool | None = None
    origin_type_id: str


class Credit(Resource, Generic16Mixin):
    """Credit."""

    attr_endpoint: ClassVar[str] = "api/v2/credits"
    attr_seq: ClassVar[str] = "credit_seq"
    credit_seq: str | None = None
    name: str
    position: str | Reference | Reference
    payee: str | Reference | Reference
    sales_order: str | Reference
    sales_transaction: str | Reference | None = None
    period: str | Reference | Reference
    credit_type: str | Reference
    value: Value
    preadjusted_value: Value
    origin_type_id: str
    reason: str | Reference | None = None
    rule: str | Reference | Reference | None = None
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
    processing_unit: str = Field(repr=False)


class Deposit(Resource, Generic16Mixin):
    """Deposit."""

    attr_endpoint: ClassVar[str] = "api/v2/deposits"
    attr_seq: ClassVar[str] = "deposit_seq"
    deposit_seq: str | None = None
    name: str
    earning_group_id: str
    earning_code_id: str
    payee: str | Reference
    position: str | Reference
    period: str | Reference
    value: Value
    preadjusted_value: Value
    origin_type_id: str
    reason: str | None = None
    business_units: list[str] | None = None
    rule: str | Reference | None = None
    deposit_date: datetime | None = None
    is_held: bool | None = None
    release_date: datetime | None = None
    pipeline_run: str | None = None
    pipeline_run_date: datetime | None = None
    processing_unit: str | None = None
    comments: str | None = None
    is_private: bool | None = None
    model_seq: str | None = None


class EarningGroupCode(Resource):
    """EarningGroupCode."""

    attr_endpoint: ClassVar[str] = "api/v2/earningGroupCodes"
    attr_seq: ClassVar[str] = "earning_group_code_seq"
    earning_group_code_seq: str | None = None
    earning_group_code: str
    earning_code_id: str
    earning_group_id: str
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class GenericClassifier(Resource, Generic16Mixin):
    """Generic Classifier."""

    attr_endpoint: ClassVar[str] = "api/v2/genericClassifiers"
    attr_seq: ClassVar[str] = "generic_classifier_seq"
    generic_classifier_seq: str | None = None
    name: str | None = None
    description: str | None = None
    classifier_id: str
    classifier_seq: str
    selector_id: str
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class GenericClassifierType(Resource):
    """Generic Classifier Type."""

    attr_endpoint: ClassVar[str] = "api/v2/genericClassifierTypes"
    attr_seq: ClassVar[str] = "generic_classifier_type_seq"
    generic_classifier_type_seq: int | None = None
    name: str


class GlobalFieldName(Resource):
    """Global Field Name."""

    attr_endpoint: ClassVar[str] = "api/v2/globalFieldNames"
    attr_seq: ClassVar[str] = "global_field_name_seq"
    global_field_name_seq: str | None = None
    name: str
    description: str | None = None
    global_field_name_data_type_length: int


# class Group(Resource):
#     """Group."""

#     attr_endpoint: ClassVar[str] = "api/v2/groups"
#     attr_seq: ClassVar[str] = "group_seq"
#     group_seq: str | None = None
#     name: str
#     description: str | None = None


class Incentive(Resource, Generic16Mixin):
    """Incentive."""

    attr_endpoint: ClassVar[str] = "api/v2/incentives"
    attr_seq: ClassVar[str] = "incentive_seq"
    incentive_seq: str | None = None
    name: str | None = None
    quota: Value | None = None
    attainment: Value | None = None
    position: str | Reference
    payee: str | Reference
    period: str | Reference
    rule: str | Reference
    value: Value
    release_date: datetime | None = None
    pipeline_run: str | None = None
    pipeline_run_date: datetime | None = None
    is_active: bool = True
    is_private: bool | None = None
    processing_unit: str | None = None
    business_units: list[str] | None = None


class Measurement(Resource, Generic16Mixin):
    """Measurement."""

    attr_endpoint: ClassVar[str] = "api/v2/measurements"
    attr_seq: ClassVar[str] = "measurement_seq"
    measurement_seq: str | None = None
    name: str
    position: str | Reference
    payee: str | Reference
    period: str | Reference
    rule: str | Reference | None = None
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


class Message(Resource):
    """Message."""

    attr_endpoint: ClassVar[str] = "api/v2/messages"
    attr_seq: ClassVar[str] = "message_seq"
    message_seq: str | None = None
    message_key: str
    message_time_stamp: datetime
    argument_count: int
    sub_category: str
    message_log: str
    module: str
    rule: str | Reference | None = None
    payee: str | Reference | None = None
    message_type: str
    run_period: str | Reference | None = None
    object_seq: str | None = None
    sales_transaction: str | None = None
    position: str | Reference | None = None
    category: str | None = None
    credit: str | None = None


class MessageLog(Resource):
    """Message Log."""

    attr_endpoint: ClassVar[str] = "api/v2/messageLogs"
    attr_seq: ClassVar[str] = "message_log_seq"
    message_log_seq: str | None = None
    source_seq: str | None = None
    component_name: str
    log_date: datetime
    log_name: str


class Participant(Resource, Generic16Mixin):
    """Participant."""

    attr_endpoint: ClassVar[str] = "api/v2/participants"
    attr_seq: ClassVar[str] = "payee_seq"
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
    event_calendar: str | Reference | None = None
    tax_id: str | None = None
    business_units: list[str] | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


# class Payment(Resource):
#     """Payment."""

#     attr_endpoint: ClassVar[str] = "api/v2/payments"
#     attr_seq: ClassVar[str] = "payment_seq"
#     payment_seq: str | None = None
#     position: str | Reference
#     payee: str | Reference
#     period: str | Reference
#     earning_group_id: str
#     earning_code_id: str
#     trial_pipeline_run: str | None = None
#     trial_pipeline_run_date: datetime | None = None
#     post_pipeline_run: str | None = None
#     post_pipeline_run_date: datetime | None = None
#     reason: str | None = None
#     value: Value
#     processingUnit: str | None = None


class PaymentMapping(Resource):
    """Payment Mapping."""

    attr_endpoint: ClassVar[str] = "api/v2/paymentMappings"
    attr_seq: ClassVar[str] = "payment_mapping_seq"
    payment_mapping_seq: str | None = None
    source_table_name: str
    source_attribute: str
    payment_attribute: str


class PaymentSummary(Resource):
    """Payment Summary."""

    attr_endpoint: ClassVar[str] = "api/v2/paymentSummarys"
    attr_seq: ClassVar[str] = "payment_summary_seq"
    payment_summary_seq: str | None = None
    position: str | Reference
    participant: str | Reference
    period: str | Reference
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


class Period(Resource):
    """Period."""

    attr_endpoint: ClassVar[str] = "api/v2/periods"
    attr_seq: ClassVar[str] = "period_seq"
    period_seq: str | None = None
    name: str
    short_name: str
    start_date: datetime
    end_date: datetime
    period_type: str | Reference
    calendar: str | Reference
    description: str | None = None
    parent: str | Reference | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class PeriodType(Resource):
    """Period Type."""

    attr_endpoint: ClassVar[str] = "api/v2/periodTypes"
    attr_seq: ClassVar[str] = "period_type_seq"
    period_type_seq: str | None = None
    name: str
    description: str | None = None
    level: int | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class Pipeline(Resource):
    """Pipeline."""

    attr_endpoint: ClassVar[str] = "api/v2/pipelines"
    attr_seq: ClassVar[str] = "pipeline_run_seq"
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
    processing_unit: str = Field(repr=False)
    period: str | Reference | None = None
    description: str | None = None
    status: const.PipelineStatus | None = None
    run_progress: float | None = None
    start_time: datetime | None = None
    stop_time: datetime | None = None
    start_date_scheduled: datetime | None = None
    batch_name: str | None = None
    priority: int | None = Field(repr=False)
    message: str | None = None
    num_errors: int | None = Field(repr=False)
    num_warnings: int | None = Field(repr=False)
    run_mode: const.ImportRunMode | const.PipelineRunMode | None = Field(
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
    stage_tables: list[Assignment] | Assignment | None = Field(None, repr=False)
    model_seq: str | None = None
    model_run: str | None = None

    @field_validator("run_progress", mode="before")
    @classmethod
    def percent_as_float(cls, value: str) -> float | None:
        """Convert percentage string to float."""
        return int(value.removesuffix("%")) / 100 if value else None


class PositionGroup(Resource):
    """Position."""

    attr_endpoint: ClassVar[str] = "api/v2/positionGroups"
    attr_seq: ClassVar[str] = "position_group_seq"
    position_group_seq: str | None = None
    name: str
    business_units: list[str] | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class PositionRelation(Resource):
    """Position Relation."""

    attr_endpoint: ClassVar[str] = "api/v2/positionRelations"
    attr_seq: ClassVar[str] = "position_relation_seq"
    position_relation_seq: str | None = None
    name: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    parent_position: str | Reference
    position_relation_type: str
    child_position: str | Reference
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class PostalCode(Resource, Generic16Mixin):
    """Postal Code."""

    attr_endpoint: ClassVar[str] = "api/v2/postalCodes"
    attr_seq: ClassVar[str] = "classifier_seq"
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


class ProcessingUnit(Resource):
    """Processing Unit."""

    attr_endpoint: ClassVar[str] = "api/v2/processingUnits"
    attr_seq: ClassVar[str] = "processing_unit_seq"
    processing_unit_seq: str | None = None
    name: str
    description: str | None = None


class Product(Resource, Generic16Mixin):
    """Product."""

    attr_endpoint: ClassVar[str] = "api/v2/products"
    attr_seq: ClassVar[str] = "classifier_seq"
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
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class Quota(Resource):
    """Quota."""

    attr_endpoint: ClassVar[str] = "api/v2/quotas"
    attr_seq: ClassVar[str] = "quota_seq"
    quota_seq: str | None = None
    calendar: str | Reference
    name: str
    description: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    unit_type: str | Reference
    model_seq: str | None = None
    business_units: list[str] | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class SalesOrder(Resource, Generic16Mixin):
    """Sales Order."""

    attr_endpoint: ClassVar[str] = "api/v2/salesOrders"
    attr_seq: ClassVar[str] = "sales_order_seq"
    sales_order_seq: str | None = None
    order_id: str
    pipeline_run: str | None = None
    business_units: list[str] | None = None
    processing_unit: str | None = None
    model_seq: str | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class SalesTransaction(Resource, Generic32Mixin):
    """Sales Transaction."""

    attr_endpoint: ClassVar[str] = "api/v2/salesTransactions"
    attr_seq: ClassVar[str] = "sales_transaction_seq"
    sales_transaction_seq: str | None = None
    sales_order: str | Reference
    line_number: Value
    sub_line_number: Value
    event_type: str | Reference
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


class User(Resource):
    """User."""

    attr_endpoint: ClassVar[str] = "api/v2/users"
    attr_seq: ClassVar[str] = "user_seq"
    user_seq: str | None = None
    id: str
    user_name: str | None = None
    description: str | None = None
    email: str | None = None
    read_only_business_unit_list: list[dict[Literal["name"], str]] | None = None
    full_access_business_unit_list: list[dict[Literal["name"], str]] | None = None
    preferred_language: str | None = None
    last_login: datetime | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class PlanComponent(Resource):
    """Plan."""

    attr_endpoint: ClassVar[str] = "api/v2/planComponents"
    attr_seq: ClassVar[str] = "plan_component_seq"
    plan_component_seq: str | None = None
    name: str
    description: str | None = None
    calendar: str | Reference
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    not_allow_update: bool = False
    model_seq: str | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class Rule(Resource):
    """Rule."""

    attr_endpoint: ClassVar[str] = "api/v2/rules"
    attr_seq: ClassVar[str] = "rule_seq"
    rule_seq: str | None = None
    name: str
    description: str | None = None
    calendar: str | Reference
    effective_start_date: datetime
    effective_end_date: datetime
    business_unit: list[BusinessUnitAssignment] | BusinessUnitAssignment | None = None
    type: RuleUsage | None = None
    not_allow_update: bool = False
    model_seq: str | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class CreditRule(Rule):
    """Alias for Rule."""


class CommissionRule(Rule):
    """Alias for Rule."""


class DepositRule(Rule):
    """Alias for Rule."""


class MeasurementRule(Rule):
    """Alias for Rule."""
