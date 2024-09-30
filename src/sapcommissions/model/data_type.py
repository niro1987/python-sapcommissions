"""Pydantic models for Data Type Resources."""

from datetime import datetime
from typing import ClassVar

from pydantic import AliasChoices, Field

from .base import Resource, ValueClass


class _DataType(Resource):
    """Base class for DataType resources.

    These attributes are inherited by all other Data Types.

    Attributes:
        data_type_seq: System Unique Identifier.
        description: Description.
        create_date: When the Data Type was first created.
        created_by: Who created the Data Type.
        modified_by: Who last modified the Data Type.
        not_allow_update: Doesn't seem to have any impact.
    """

    attr_seq: ClassVar[str] = "data_type_seq"
    data_type_seq: str | None = None
    description: str | None = None
    create_date: datetime | None = Field(None, exclude=True, repr=False)
    created_by: str | None = Field(None, exclude=True, repr=False)
    modified_by: str | None = Field(None, exclude=True, repr=False)
    not_allow_update: bool | None = None


class CreditType(_DataType):
    """Credit Type.

    Attributes:
        credit_type_id: ID of the Credit Type.
    """

    attr_endpoint: ClassVar[str] = "api/v2/creditTypes"
    credit_type_id: str = Field(validation_alias=AliasChoices("creditTypeId", "id"))


class EarningCode(_DataType):
    """Earning Code.

    Attributes:
        earning_code_id: ID of the Earning Code.
    """

    attr_endpoint: ClassVar[str] = "api/v2/earningCodes"
    earning_code_id: str = Field(validation_alias=AliasChoices("earningCodeId", "id"))


class EarningGroup(_DataType):
    """Earning Group.

    Attributes:
        earning_group_id: ID of the Earning Group.
    """

    attr_endpoint: ClassVar[str] = "api/v2/earningGroups"
    earning_group_id: str = Field(validation_alias=AliasChoices("earningGroupId", "id"))


class EventType(_DataType):
    """Event Type.

    Attributes:
        event_type_id: ID of the Event Type.
    """

    attr_endpoint: ClassVar[str] = "api/v2/eventTypes"
    event_type_id: str = Field(validation_alias=AliasChoices("eventTypeId", "id"))


class FixedValueType(_DataType):
    """Fixed Value Type.

    Attributes:
        fixed_value_type_id: ID of the Fixed Value Type.
    """

    attr_endpoint: ClassVar[str] = "api/v2/fixedValueTypes"
    fixed_value_type_id: str = Field(
        validation_alias=AliasChoices("fixedValueTypeId", "id")
    )


class PositionRelationType(_DataType):
    """Position Relation Type.

    Attributes:
        name: Name of the relation type.
    """

    attr_endpoint: ClassVar[str] = "api/v2/positionRelationTypes"
    name: str


class Reason(_DataType):
    """Reason.

    Attributes:
        reason_id: ID of the Reason.
    """

    attr_endpoint: ClassVar[str] = "api/v2/reasons"
    reason_id: str = Field(validation_alias=AliasChoices("reasonId", "id"))


class StatusCode(_DataType):
    """Status Code.

    Attributes:
        status: The status.
        name: Name of the status.
        type: type of status.
        is_active: If the status is active.
    """

    attr_endpoint: ClassVar[str] = "api/v2/statusCodes"
    status: str
    name: str | None = None
    type: str | None = None
    is_active: bool = True


class UnitType(_DataType):
    """Unit Type.

    Attributes:
        unit_type_seq: System Unique Identifier of the Unit Type.
        name: Name of the Unit Type
        symbol: Symbol used to represent the unit type.
        scale: How many decimals to store.
        reporting_scale: How many decimals to report.
        position_of_symbol: Where to display the symbol.
        currency_locale: Currency in locale.
        value_class: Class of Value.
        formatting: How to represent the Value.
    """

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
