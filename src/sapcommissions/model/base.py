"""Pydantic models for Python SAP Commissions Client.

These classes are generally not used directly but can be usefull
for type checking and type hints. Used to inherrit function on
all other models.
"""

from datetime import datetime
from importlib import import_module
from inspect import isclass
from types import ModuleType
from typing import Any, ClassVar, Literal, get_args, get_origin

from pydantic import (
    AliasGenerator,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)
from pydantic.alias_generators import to_camel
from pydantic.fields import FieldInfo


class _BaseModel(BaseModel):
    """BaseModel inherited from ``pydantic.BaseModel``.

    Contains the primary model_config which is required
    for Pydantic to convert field names between
    snake_case and camelCase when sending and recieving
    json data from/to the SAP Commissions tenant.
    """

    model_config: ClassVar[ConfigDict] = ConfigDict(
        str_strip_whitespace=True,
        str_min_length=1,
        extra="allow",
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
        alias_generator=AliasGenerator(alias=to_camel),
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

    @classmethod
    def typed_fields(
        cls,
        typed: type | tuple[type, ...],
    ) -> dict[str, FieldInfo]:
        """Return model fields of the specified type.

        This method can be usefull when converting data types for
        example.

        Returns:
            A dictionary of attributes annotated with the specified type
            where the keys are attribute names and the values are
            `FieldInfo` objects.
        """
        model_fields: dict[str, FieldInfo] = cls.model_fields
        fields: dict[str, FieldInfo] = {}

        def _process_type(
            field_name: str,
            field_info: FieldInfo,
            field_type: type | None,
        ) -> None:
            """Recursively process types."""
            if field_type is None:
                return

            if get_origin(field_type) is None:
                if isclass(field_type) and issubclass(field_type, typed):
                    fields[field_name] = field_info
                return

            # If the field_type has an origin, process its generic arguments recursively
            for arg in get_args(field_type):
                _process_type(field_name, field_info, arg)

        # Iterate through each field and process its type
        for field_name, field_info in model_fields.items():
            _process_type(field_name, field_info, field_info.annotation)

        return fields


class Endpoint(_BaseModel):
    """Base class for resources that can connect with the client.

    Parameters:
        attr_endpoint (str): URI endpoint to connect with
            tenant. Must follow format ``api/v2/nameOfResource``.
            Used by the client to construct the full request url.
    """

    attr_endpoint: ClassVar[str]

    @classmethod
    def expands(cls) -> dict[str, FieldInfo]:
        """Return model fields that refer to another model class.

        This function is primarily used by the client to add the
        ``expand`` parameter to the request.

        Returns:
            A dictionary of attributes that can be expanded
            where the keys are attribute names and the values are
            ``FieldInfo`` objects.
        """
        return cls.typed_fields(Expandable)


class Resource(Endpoint):
    """Base class for a resource.

    Every resource has it's own attribute that uniquely
    identifies the object on the tenant. Inheritance of
    this class allows us to refer to the system unique
    identifier without having to address it directly.

    Example:
        Attributes ``seq`` and ``credit_seq`` are
        equal::

            assert Credit.seq == Credit.credit_seq

    Parameters:
        attr_seq (str): Name of attribute that contains the
            system unique identifier (seq).
    """

    attr_seq: ClassVar[str]

    @property
    def seq(self) -> str | None:
        """System unique identifier (seq) of the resource instance."""
        return getattr(self, self.attr_seq)


class ValueUnitType(_BaseModel):
    """Unit Type of for ``Value``.

    Parameters:
        name (str): Name of the unit type.
        unit_type_seq (str): System unique identifier.
    """

    name: str
    unit_type_seq: str


class Value(_BaseModel):
    """Value object used by all numeric fields.

    Parameters:
        value (int | float | None): The amount.
        unit_type (ValueUnitType): Type of amount.
    """

    value: int | float | None
    unit_type: ValueUnitType


class ValueClass(_BaseModel):
    """Value Class, used only by ``UnitType``.

    Parameters:
        display_name (str): Name of the value class.
    """

    display_name: str


class AdjustmentContext(_BaseModel):
    """Adjustment Context for ``SalesTransaction``.

    Used only when updating the value of a ``SalesTransaction``.

    Parameters:
        adjust_type_flag (Literal["adjustTo", "adjustBy", "reset"]):
            - ``adjustTo``
            - ``adjustBy``
            - ``reset``
        adjust_to_value (Value | None): Adjust value to this amount.
        adjust_by_value (Value | None): Adjust value by this amount.
        comment (str | None): Adjustment comment.
    """

    adjust_type_flag: Literal["adjustTo", "adjustBy", "reset"]
    adjust_to_value: Value | None = None
    adjust_by_value: Value | None = None
    comment: str | None = None


class Generic16Mixin(_BaseModel):
    """Mixin to add generic fields to a model."""

    ga1: str | None = Field(None, alias="genericAttribute1")
    ga2: str | None = Field(None, alias="genericAttribute2")
    ga3: str | None = Field(None, alias="genericAttribute3")
    ga4: str | None = Field(None, alias="genericAttribute4")
    ga5: str | None = Field(None, alias="genericAttribute5")
    ga6: str | None = Field(None, alias="genericAttribute6")
    ga7: str | None = Field(None, alias="genericAttribute7")
    ga8: str | None = Field(None, alias="genericAttribute8")
    ga9: str | None = Field(None, alias="genericAttribute9")
    ga10: str | None = Field(None, alias="genericAttribute10")
    ga11: str | None = Field(None, alias="genericAttribute11")
    ga12: str | None = Field(None, alias="genericAttribute12")
    ga13: str | None = Field(None, alias="genericAttribute13")
    ga14: str | None = Field(None, alias="genericAttribute14")
    ga15: str | None = Field(None, alias="genericAttribute15")
    ga16: str | None = Field(None, alias="genericAttribute16")
    gn1: Value | None = Field(None, alias="genericNumber1")
    gn2: Value | None = Field(None, alias="genericNumber2")
    gn3: Value | None = Field(None, alias="genericNumber3")
    gn4: Value | None = Field(None, alias="genericNumber4")
    gn5: Value | None = Field(None, alias="genericNumber5")
    gn6: Value | None = Field(None, alias="genericNumber6")
    gd1: datetime | None = Field(None, alias="genericDate1")
    gd2: datetime | None = Field(None, alias="genericDate2")
    gd3: datetime | None = Field(None, alias="genericDate3")
    gd4: datetime | None = Field(None, alias="genericDate4")
    gd5: datetime | None = Field(None, alias="genericDate5")
    gd6: datetime | None = Field(None, alias="genericDate6")
    gb1: bool | None = Field(None, alias="genericBoolean1")
    gb2: bool | None = Field(None, alias="genericBoolean2")
    gb3: bool | None = Field(None, alias="genericBoolean3")
    gb4: bool | None = Field(None, alias="genericBoolean4")
    gb5: bool | None = Field(None, alias="genericBoolean5")
    gb6: bool | None = Field(None, alias="genericBoolean6")


class Generic32Mixin(Generic16Mixin):
    """Mixin to add generic fields to a model."""

    ga17: str | None = Field(None, alias="genericAttribute17")
    ga18: str | None = Field(None, alias="genericAttribute18")
    ga19: str | None = Field(None, alias="genericAttribute19")
    ga20: str | None = Field(None, alias="genericAttribute20")
    ga21: str | None = Field(None, alias="genericAttribute21")
    ga22: str | None = Field(None, alias="genericAttribute22")
    ga23: str | None = Field(None, alias="genericAttribute23")
    ga24: str | None = Field(None, alias="genericAttribute24")
    ga25: str | None = Field(None, alias="genericAttribute25")
    ga26: str | None = Field(None, alias="genericAttribute26")
    ga27: str | None = Field(None, alias="genericAttribute27")
    ga28: str | None = Field(None, alias="genericAttribute28")
    ga29: str | None = Field(None, alias="genericAttribute29")
    ga30: str | None = Field(None, alias="genericAttribute30")
    ga31: str | None = Field(None, alias="genericAttribute31")
    ga32: str | None = Field(None, alias="genericAttribute32")


class Expandable(_BaseModel):
    """Indicates expandable field.

    Any model field that is annotated with a subclass of
    ``Expandable`` will be added to the ``expand`` parameter
    when sending requests to the tenant.
    """


class Reference(Expandable):
    """Expanded reference to a resource.

    Parameters:
        key (str): System unique identifier for the referred resource.
        display_name (str): Name of the referred resource.
        object_type (type[model.Resource]): Class of the referred resource.
        key_string (str): Seems to always be the same as ``key``.
        logical_keys (dict[str, str | int | Value | Any]): Some key
            attributes of the referred resource.
    """

    key: str
    display_name: str
    object_type: type[Resource]
    key_string: str | None = None
    logical_keys: dict[str, str | int | Value | Any]

    @field_validator("object_type", mode="before")
    @classmethod
    def convert_object_type(cls, value: str) -> type[Resource]:
        """Convert string object_type to class."""
        module: ModuleType = import_module("sapcommissions.model")
        if not (obj := getattr(module, value, None)):
            raise ValueError(f"Unknown object type: {value}")
        if issubclass(obj, Resource):
            return obj
        raise ValueError(f"Invalid object type: {value}")

    def __str__(self) -> str:
        """Return key value."""
        return self.key


class SalesTransactionAssignment(Expandable, Generic16Mixin):
    """Expanded reference to a transaction assignment.

    Parameters:
        payee_id (str | None): Participant ID assigned to the transaction.
        position_name (str | None): Position Name assigned to the transaction.
        title_name (str | None): Title Name assigned to the transaction.
        sales_order (str | None): Order ID of the transaction.
        sales_transaction_seq (str): System unique identifier of the
            transaction.
        set_number (int | None): Index of the Assignment.
        compensation_date (datetime | None): Compensation Date of the
            transaction.
        processing_unit (str | None): System unique identifier of the
            Processing Unit.
        ga{1-16} (str | None): Generic Attributes.
        gn{1-6} (Value | None): Generic Numbers.
        gd{1-6} (datetime | None): Generic Dates.
        gb{1-6} (bool | None): Generic Booleans.
    """

    payee_id: str | None = None
    position_name: str | None = None
    title_name: str | None = None
    sales_order: str
    sales_transaction_seq: str
    set_number: int | None = None
    compensation_date: datetime | None = None
    processing_unit: str | None = None


class Assignment(_BaseModel):
    """Assignment.

    Used by ``Pipeline`` to refer to stage tables and by
    ``Plan``, ``Title`` and ``Position`` to refer to
    Variable Assignments.

    Parameters:
        key (str | None): Not sure really.
        owned_key (str | None): Also not sure really.

    TODO: Is this an expandable reference?
    """

    key: str | None = None
    owned_key: str | None = None


class BusinessUnitAssignment(_BaseModel):
    """Business Unit Assignment.

    Used by ``AuditLog`` and ``Rule`` to refer to
    Business Units.

    Parameters:
        mask (int): Not sure really.
        smask (int): Seems to be the same as mask.

    TODO: Is this an expandable reference?
    """

    mask: int
    smask: int


class RuleUsage(_BaseModel):
    """Rule Usage.

    Used by ``Rule`` and ``Rule Elements`` for some reason.

    Parameters:
        id (str): ID
        name (str): Name

    TODO: Is this an expandable reference?
    """

    id: str
    name: str


class RuleUsageList(_BaseModel):
    """List of RuleUsage.

    Parameters:
        children (list[RuleUsage]): List of RuleUsage elements.

    TODO: Is this an expandable reference?
    TODO: Make this class accessible as iterator of ``RuleUsage``.
    """

    children: list[RuleUsage]
