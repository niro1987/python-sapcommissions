"""RuleElementOwner models for Python SAP Commissions Client."""

from datetime import datetime
from typing import ClassVar

from pydantic import Field

from .base import (
    Assignment,
    Generic16Mixin,
    Reference,
    Resource,
)


class _RuleElementOwner(Resource):
    """Base class for Rule Element Owner resources."""

    attr_seq: ClassVar[str] = "rule_element_owner_seq"
    rule_element_owner_seq: str | None = None
    name: str
    description: str | None = None
    effective_start_date: datetime
    effective_end_date: datetime
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    created_by: str | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)
    business_units: list[str] | None = None
    variable_assignments: list[Assignment] | Assignment | None = None
    model_seq: str | None = None


class Plan(_RuleElementOwner):
    """Plan."""

    attr_endpoint: ClassVar[str] = "api/v2/plans"
    calendar: str | Reference


class Position(_RuleElementOwner, Generic16Mixin):
    """Position."""

    attr_endpoint: ClassVar[str] = "api/v2/positions"
    credit_start_date: datetime | None = None
    credit_end_date: datetime | None = None
    processing_start_date: datetime | None = None
    processing_end_date: datetime | None = None
    target_compensation: dict | None = None
    processing_unit: str | None = None
    manager: str | Reference | None = None
    title: str | Reference | None = None
    plan: str | Reference | None = None
    position_group: str | Reference | None = None
    payee: str | Reference | None = None


class Title(_RuleElementOwner, Generic16Mixin):
    """Title."""

    attr_endpoint: ClassVar[str] = "api/v2/titles"
    plan: str | Reference | None = None
