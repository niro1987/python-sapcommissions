"""DataType models for Python SAP Commissions Client."""

from datetime import datetime
from typing import ClassVar

from pydantic import AliasChoices, Field

from .base import Resource, ValueClass


class _DataType(Resource):
    """Base class for Data Type resources."""

    attr_seq: ClassVar[str] = "data_type_seq"
    data_type_seq: str | None = None
    description: str | None = None
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    created_by: str | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)
    not_allow_update: bool | None = None


class CreditType(_DataType):
    """Credit Type."""

    attr_endpoint: ClassVar[str] = "api/v2/creditTypes"
    credit_type_id: str = Field(validation_alias=AliasChoices("creditTypeId", "id"))


class EarningCode(_DataType):
    """Earning Code."""

    attr_endpoint: ClassVar[str] = "api/v2/earningCodes"
    earning_code_id: str = Field(validation_alias=AliasChoices("earningCodeId", "id"))


class EarningGroup(_DataType):
    """Earning Group."""

    attr_endpoint: ClassVar[str] = "api/v2/earningGroups"
    earning_group_id: str = Field(validation_alias=AliasChoices("earningGroupId", "id"))


class EventType(_DataType):
    """Class representation of an Event Type."""

    attr_endpoint: ClassVar[str] = "api/v2/eventTypes"
    event_type_id: str = Field(validation_alias=AliasChoices("eventTypeId", "id"))


class FixedValueType(_DataType):
    """Fixed Value Type."""

    attr_endpoint: ClassVar[str] = "api/v2/fixedValueTypes"
    fixed_value_type_id: str = Field(
        validation_alias=AliasChoices("fixedValueTypeId", "id")
    )


class PositionRelationType(_DataType):
    """Position Relation Type."""

    attr_endpoint: ClassVar[str] = "api/v2/positionRelationTypes"
    name: str


class Reason(_DataType):
    """Reason."""

    attr_endpoint: ClassVar[str] = "api/v2/reasons"
    reason_id: str = Field(validation_alias=AliasChoices("reasonId", "id"))


class StatusCode(_DataType):
    """Status Code."""

    attr_endpoint: ClassVar[str] = "api/v2/statusCodes"
    name: str | None = None
    type: str | None = None
    status: str
    is_active: bool = True


class UnitType(_DataType):
    """Class representation of a Unit Type."""

    attr_endpoint: ClassVar[str] = "api/v2/unitTypes"
    unit_type_seq: str
    name: str
    symbol: str | None = None
    scale: int
    reporting_scale: int
    position_of_symbol: int
    currency_locale: str | None = None
    value_class: ValueClass
    formatting: str | None = None
