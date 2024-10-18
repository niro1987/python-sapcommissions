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

    TODO: ``variable_assignments`` should be ``Reference``?
    TODO: ``business_units`` should be ``Reference``?
    """

    attr_seq: ClassVar[str] = 'rule_element_owner_seq'
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

    Parameters:
        rule_element_owner_seq (str | None): System Unique Identifier.
        name (str): Name of the plan.
        description (str | None): Description of the plan.
        calendar (str | Reference): Reference to ``Calendar`` associated
            with the plan.
        effective_start_date (datetime): Effective start date of the plan
            version.
        effective_end_date (datetime): Effective end date of the plan version.
        create_date (datetime | None): Date when plan was created.
        created_by (str | None): User ID that created the plan.
        modified_by (str | None): User ID that last modified the plan.
        business_units (list[str] | None): Business units associated with the
            plan.
        variable_assignments (list[Assignment] | Assignment | None): Variable
            Assignments on the plan level.
        model_seq (str | None): System Unique Identifier for the model.

    TODO: Add GenericMixin?
    TODO: is ``variable_assignments`` expandable?
    """

    attr_endpoint: ClassVar[str] = 'api/v2/plans'
    calendar: str | Reference


class Position(_RuleElementOwner, Generic16Mixin):
    """Position.

    TODO: ``target_compensation`` is ``Value``?
    TODO: ``processing_unit`` should be ``Reference``?
    """

    attr_endpoint: ClassVar[str] = 'api/v2/positions'
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
    """Title."""

    attr_endpoint: ClassVar[str] = 'api/v2/titles'
    plan: str | Reference | None = None
