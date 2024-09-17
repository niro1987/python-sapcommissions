"""Base models for Python SAP Commissions Client."""

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


class _BaseModel(BaseModel):
    """BaseModel for SAP Commissions."""

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


class Endpoint(_BaseModel):
    """BaseModel for an Endpoint."""

    attr_endpoint: ClassVar[str]

    @classmethod
    def expands(cls) -> list[str]:
        """Return list of model fields that refer to onther resource."""
        reference_fields: list[str] = []
        for field_name, field_type in cls.__annotations__.items():
            if get_origin(field_type) is not None:
                for arg in get_args(field_type):
                    if isclass(arg) and issubclass(arg, Reference):
                        reference_fields.append(field_name)
                        break
            elif isclass(field_type) and issubclass(field_type, Reference):
                reference_fields.append(field_name)

        return reference_fields


class Resource(Endpoint):
    """Base class for a Resource."""

    attr_seq: ClassVar[str]

    @property
    def seq(self) -> str | None:
        """Return the `seq` attribute value for the resource."""
        return getattr(self, self.attr_seq)


class Assignment(_BaseModel):
    """BaseModel for Assignment."""

    key: str | None = None
    owned_key: str | None = None


class BusinessUnitAssignment(_BaseModel):
    """BaseModel for BusinessUnitAssignment."""

    mask: int
    smask: int


class RuleUsage(_BaseModel):
    """BaseModel for RuleUsage."""

    id: str
    name: str


class RuleUsageList(_BaseModel):
    """BaseModel for RuleUsage lists."""

    children: list[RuleUsage]


class ValueUnitType(_BaseModel):
    """BaseModel for UnitType."""

    name: str
    unit_type_seq: str


class Value(_BaseModel):
    """BaseModel for Value."""

    value: int | float | None
    unit_type: ValueUnitType


class ValueClass(_BaseModel):
    """BaseModel for ValueClass."""

    display_name: str


class AdjustmentContext(_BaseModel):
    """Adjustment Context for a Sales Transaction."""

    adjust_type_flag: Literal["adjustTo", "adjustBy", "reset"]
    adjust_to_value: Value | None = None
    adjust_by_value: Value | None = None
    comment: str | None = None


class Generic16Mixin(_BaseModel):
    """Mixin to add Generic Attributes to a model."""

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
    """Mixin to add extended Generic Attributes to a model."""

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


class Reference(_BaseModel):
    """Pydantic BaseModel for reference to another resource."""

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
