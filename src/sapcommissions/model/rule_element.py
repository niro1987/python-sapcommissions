"""RuleElement models for Python SAP Commissions Client."""

from datetime import datetime
from typing import ClassVar

from pydantic import Field

from .base import (
    Assignment,
    Generic16Mixin,
    Reference,
    Resource,
    RuleUsage,
    RuleUsageList,
    Value,
)


class _RuleElement(Resource):
    """Base class for Rule Element resources."""

    attr_seq: ClassVar[str] = "rule_element_seq"
    rule_element_seq: str | None = None
    name: str
    description: str | None = None
    calendar: str | Reference | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    not_allow_update: bool = False
    model_seq: str | None = None
    reference_class_type: str | None = None
    return_type: str | None = None
    owning_element: str | None = None
    rule_usage: RuleUsageList | RuleUsage | None = None
    input_signature: str | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)


class Category(_RuleElement, Generic16Mixin):
    """Category."""

    attr_endpoint: ClassVar[str] = "api/v2/categories"
    owner: str | Reference
    parent: str | Reference | None = None


class FixedValue(_RuleElement):
    """Fixed Value."""

    attr_endpoint: ClassVar[str] = "api/v2/fixedValues"
    value: Value | None = None
    fixed_value_type: str | Reference | None = None
    period_type: str | Reference | None = None


class CFixedValue(FixedValue):
    """Alias for FixedValue."""


class Formula(_RuleElement):
    """Formula."""

    attr_endpoint: ClassVar[str] = "api/v2/formulas"


class FixedValueVariable(_RuleElement):
    """Fixed Value Variable."""

    attr_endpoint: ClassVar[str] = "api/v2/fixedValueVariables"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None


class LookUpTableVariable(_RuleElement):
    """LookUp Table Variable."""

    attr_endpoint: ClassVar[str] = "api/v2/lookUpTableVariables"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None


class RateTable(_RuleElement):
    """Rate Table."""

    attr_endpoint: ClassVar[str] = "api/v2/rateTables"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None
    return_unit_type: str | Reference | None = None


class RateTableVariable(_RuleElement):
    """Rate Table Variable."""

    attr_endpoint: ClassVar[str] = "api/v2/rateTableVariables"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None


class RelationalMDLT(_RuleElement):
    """Relational MDLT."""

    attr_endpoint: ClassVar[str] = "api/v2/relationalMDLTs"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None
    return_unit_type: str | Reference | None = None
    indices: list[Assignment] | Assignment | None = None
    treat_null_as_zero: bool | None = None
    expression_type_counts: str | None = None
    dimensions: list[Assignment] | Assignment | None = None


class Territory(_RuleElement):
    """Territory."""

    attr_endpoint: ClassVar[str] = "api/v2/territories"


class TerritoryVariable(_RuleElement):
    """Territory Variable."""

    attr_endpoint: ClassVar[str] = "api/v2/territoryVariables"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None


class Variable(_RuleElement):
    """Variable."""

    attr_endpoint: ClassVar[str] = "api/v2/variables"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None
