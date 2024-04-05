"""Test for SAP Commissions Models."""
# pylint: disable=protected-access

import logging
from collections.abc import Generator
from inspect import isclass
from typing import TypeVar

import pytest
from pydantic import BaseModel
from pydantic.fields import FieldInfo, ModelPrivateAttr

from sapcommissions import model

LOGGER: logging.Logger = logging.getLogger(__name__)
T = TypeVar("T", bound="model._Resource")


def list_resource_cls() -> Generator[type[model._Resource], None, None]:
    """List all resource classes in the model module."""
    for name in dir(model):
        obj = getattr(model, name)
        if (
            isclass(obj)
            and issubclass(obj, model._Resource)
            and not obj.__name__.startswith("_")
        ):
            yield obj


@pytest.mark.parametrize(
    "resource_cls",
    list_resource_cls(),
)
def test_resource_basics(
    resource_cls: type[T],
) -> None:
    """Test list resources."""
    assert issubclass(resource_cls, BaseModel), "resource is not a pydantic model"
    assert issubclass(
        resource_cls, model._Base
    ), "resource is not a subclass of '_Base'"

    # _endpoint
    assert hasattr(
        resource_cls, "_endpoint"
    ), "resource does not have attribute '_endpoint'"
    endpoint: ModelPrivateAttr = resource_cls.__private_attributes__["_endpoint"]
    assert isinstance(
        endpoint.default, str
    ), "resource does not have a default value for '_endpoint'"
    assert endpoint.default.startswith(
        "api/v2/"
    ), "_endpoint should start with 'api/v2/'"

    # _attr_seq
    assert hasattr(
        resource_cls, "_attr_seq"
    ), "resource does not have attribute '_attr_seq'"
    attr_seq: ModelPrivateAttr = resource_cls.__private_attributes__["_attr_seq"]
    assert isinstance(
        attr_seq.default, str
    ), "resource does not have a default value for '_attr_seq'"
    assert len(attr_seq.default), "_attr_seq should not be an emptry string"
    assert attr_seq.default.endswith("Seq"), "_attr_seq should end with 'Seq'"
    if issubclass(resource_cls, model._RuleElementOwner):
        assert attr_seq.default == "ruleElementOwnerSeq"

    # seq field
    assert attr_seq.default in resource_cls.model_fields
    seq_field: FieldInfo = resource_cls.model_fields[attr_seq.default]
    assert seq_field.annotation == str | None
    assert seq_field.default is None
