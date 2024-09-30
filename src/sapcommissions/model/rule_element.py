"""Pydantic models for Rule Element Resources."""

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
    """Base class for Rule Element resources.

    These attributes are inherited by all other Rule Elements.

    Attributes:
        rule_element_seq: System Unique Identifier.
        name: Name.
        description: Description.
        calendar: Reference to ``Calendar``.
        effective_start_date: Effective Start Date.
        effective_end_date: Effective End Date.
        business_units: Business Units.
        not_allow_update: Doesn't seem to have any impact.
        reference_class_type: Type of element.
        return_type: Return type.
        owning_element: Not sure.
        rule_usage: Usage.
        input_signature: Input signature.
        created_by: Who created the element.
        create_date: When the element was first created.
        modified_by: Who last modified the element.
        model_seq: System Unique Identifier for the model.

        TODO: What does ``owning_element`` represent?
    """

    attr_seq: ClassVar[str] = "rule_element_seq"
    rule_element_seq: str | None = None
    name: str
    description: str | None = None
    calendar: str | Reference | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    business_units: list[str] | None = None
    not_allow_update: bool = False
    reference_class_type: str | None = None
    return_type: str | None = None
    owning_element: str | None = None
    rule_usage: RuleUsageList | RuleUsage | None = None
    input_signature: str | None = None
    created_by: str | None = Field(None, exclude=True, repr=False)
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)
    model_seq: str | None = None


class Category(_RuleElement, Generic16Mixin):
    """Category.

    Attributes:
        owner: Reference to ``RuleElementOwner``.
        parent: Reference to parent ``Category``.
    """

    attr_endpoint: ClassVar[str] = "api/v2/categories"
    owner: str | Reference
    parent: str | Reference | None = None


class FixedValue(_RuleElement):
    """Fixed Value.

    Attributes:
        value: The value.
        fixed_value_type: Reference to ``ValueType``.
        period_type: Reference to ``PeriodType``.
    """

    attr_endpoint: ClassVar[str] = "api/v2/fixedValues"
    value: Value | None = None
    fixed_value_type: str | Reference | None = None
    period_type: str | Reference | None = None


class CFixedValue(FixedValue):
    """Alias for ``FixedValue``."""


class Formula(_RuleElement):
    """Formula."""

    attr_endpoint: ClassVar[str] = "api/v2/formulas"


class FixedValueVariable(_RuleElement):
    """Fixed Value Variable.

    Attributes:
        default_element: Reference to default ``FixedValue``.
        required_period_type: Reference to ``PeriodType``.
    """

    attr_endpoint: ClassVar[str] = "api/v2/fixedValueVariables"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None


class LookUpTableVariable(_RuleElement):
    """LookUp Table Variable.

    Attributes:
        default_element: Reference to default ``RelationalMDLT``.
        required_period_type: Reference to ``PeriodType``.
    """

    attr_endpoint: ClassVar[str] = "api/v2/lookUpTableVariables"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None


class RateTable(_RuleElement):
    """Rate Table.

    Attributes:
        default_element: Reference to default ``RelationalMDLT``.
        required_period_type: Reference to ``PeriodType``.
        return_unit_type: Reference to ``UnitType`` that this
            table returns.

    TODO: Does this endpoint return ``default_element``?
    """

    attr_endpoint: ClassVar[str] = "api/v2/rateTables"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None
    return_unit_type: str | Reference | None = None


class RateTableVariable(_RuleElement):
    """Rate Table Variable.

    Attributes:
        default_element: Reference to default ``RelationalMDLT``.
        required_period_type: Reference to ``PeriodType``.
    """

    attr_endpoint: ClassVar[str] = "api/v2/rateTableVariables"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None


class RelationalMDLT(_RuleElement):
    """Relational MDLT.

    Multi Dimensional Lookup Table.

    Attributes:
        default_element: Reference to default ``RelationalMDLT``.
        required_period_type: Reference to ``PeriodType``.
        return_unit_type: Reference to ``UnitType`` that this
            table returns.
        treat_null_as_zero: Wether the Lookup Table returns a zero
            ``Value`` if the combination of dimensions is empty
            or does not exist.
        dimensions: The dimensions in the table.
        indices: Table indices of the table.
        expression_type_counts: Not sure.

    TODO: Does this endpoint return ``default_element``?
    TODO: Are ``dimensions`` and ``indices`` expandable?
    TODO: What does ``expression_type_counts`` represent?
    """

    attr_endpoint: ClassVar[str] = "api/v2/relationalMDLTs"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None
    return_unit_type: str | Reference | None = None
    treat_null_as_zero: bool | None = None
    dimensions: list[Assignment] | Assignment | None = None
    indices: list[Assignment] | Assignment | None = None
    expression_type_counts: str | None = None


class Territory(_RuleElement):
    """Territory."""

    attr_endpoint: ClassVar[str] = "api/v2/territories"


class TerritoryVariable(_RuleElement):
    """Territory Variable.

    Attributes:
        default_element: Reference to default ``Territory``.
        required_period_type: Reference to ``PeriodType``.
    """

    attr_endpoint: ClassVar[str] = "api/v2/territoryVariables"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None


class Variable(_RuleElement):
    """Variable.

    Attributes:
        default_element: Reference to default element.
        required_period_type: Reference to ``PeriodType``.

    TODO: What does ``default_element`` refer to?
    """

    attr_endpoint: ClassVar[str] = "api/v2/variables"
    default_element: str | Reference | None = None
    required_period_type: str | Reference | None = None
