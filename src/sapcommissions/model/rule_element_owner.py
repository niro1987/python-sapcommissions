"""Pydantic models for Rule Element Owner Resources."""

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
    """Base class for Rule Element Owner resources.

    These attributes are inherited by all other Rule Element Owners.

    Attributes:
        rule_element_owner_seq: System Unique Identifier.
        name: Name.
        description: Description.
        effective_start_date: Effective Start Date.
        effective_end_date: Effective End Date.
        create_date: When the element was first created.
        created_by: Who created the element.
        modified_by: Who last modified the element.
        business_units: Business Units.
        variable_assignments: Assigned variables.
        model_seq: System Unique Identifier for the model.

    TODO: ``variable_assignments`` should be ``Reference``?
    TODO: ``business_units`` should be ``Reference``?
    """

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
    """Plan.

    Attributes:
        calendar: Reference to ``Calendar``.
    """

    attr_endpoint: ClassVar[str] = "api/v2/plans"
    calendar: str | Reference


class Position(_RuleElementOwner, Generic16Mixin):
    """Position.

    Attributes:
        payee: Reference to ``Participant``.
        plan: Reference to ``Plan``.
        title: Reference to ``Title``.
        manager: Reference to ``Position`` of manager.
        position_group: Reference to ``PositionGroup``.
        target_compensation: Target Compensation.
        credit_start_date: Credit Start Date.
        credit_end_date: Credit End Date.
        processing_start_date: Processing Start Date.
        processing_end_date: Processing End Date.
        processing_unit: system Unique Identifier of Processing Unit.

    TODO: ``target_compensation`` is ``Value``?
    TODO: ``processing_unit`` should be ``Reference``?
    """

    attr_endpoint: ClassVar[str] = "api/v2/positions"
    payee: str | Reference | None = None
    plan: str | Reference | None = None
    title: str | Reference | None = None
    manager: str | Reference | None = None
    position_group: str | Reference | None = None
    target_compensation: dict | None = None
    credit_start_date: datetime | None = None
    credit_end_date: datetime | None = None
    processing_start_date: datetime | None = None
    processing_end_date: datetime | None = None
    processing_unit: str | None = None


class Title(_RuleElementOwner, Generic16Mixin):
    """Title.

    Attributes:
        plan: Reference to ``Plan``.
    """

    attr_endpoint: ClassVar[str] = "api/v2/titles"
    plan: str | Reference | None = None
