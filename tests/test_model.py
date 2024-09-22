"""Test for SAP Commissions Models."""
# pylint: disable=protected-access

import logging
from typing import Any, ClassVar

import pytest
from pydantic import AliasChoices, BaseModel, Field
from pydantic.fields import FieldInfo

from sapcommissions.model.base import Endpoint, Reference, Resource
from sapcommissions.model.pipeline import _PipelineJob

from tests.conftest import list_endpoint_cls, list_pipeline_job_cls, list_resource_cls

LOGGER: logging.Logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "endpoint_cls",
    list_endpoint_cls(),
)
def test_endpoint_basics(
    endpoint_cls: type[Endpoint],
) -> None:
    """Test endpoints."""
    assert issubclass(
        endpoint_cls,
        BaseModel,
    ), "endpoint is not a pydantic model"
    assert issubclass(
        endpoint_cls,
        BaseModel,
    ), "endpoint is not a subclass of '_BaseModel'"
    assert issubclass(
        endpoint_cls,
        Endpoint,
    ), "endpoint is not a subclass of '_Endpoint'"

    # endpoint
    assert hasattr(
        endpoint_cls,
        "attr_endpoint",
    ), "resource does not have attribute 'attr_endpoint'"
    if not endpoint_cls.attr_endpoint.startswith("api/v2/"):
        LOGGER.warning("Endpoint possibly incorrect: %s", endpoint_cls.attr_endpoint)


@pytest.mark.parametrize(
    "resource_cls",
    list_resource_cls(),
)
def test_resource_basics(
    resource_cls: type[Resource],
) -> None:
    """Test resources."""
    # enpoint subclass
    assert issubclass(
        resource_cls,
        Endpoint,
    ), "resource is not a subclass of '_Endpoint'"
    assert issubclass(
        resource_cls,
        Resource,
    ), "resource is not a subclass of '_Resource'"

    # attr_seq
    assert hasattr(
        resource_cls,
        "attr_seq",
    ), "resource does not have attribute 'attr_seq'"
    assert resource_cls.attr_seq.endswith("_seq"), "_attr_seq should end with '_seq'"
    assert resource_cls.attr_seq in resource_cls.model_fields
    seq_field: FieldInfo = resource_cls.model_fields[resource_cls.attr_seq]
    assert seq_field.annotation in (
        int | None,
        str | None,
    ), "Invalid seq field type"

    # expands class method
    assert hasattr(
        resource_cls,
        "expands",
    ), "resource does not have class method 'expands'"

    expands = resource_cls.expands()
    assert isinstance(expands, dict), "'expands' should return a dict"
    assert all(
        isinstance(field, str) for field in expands
    ), "Invalid field type in 'expands' dict"
    assert all(
        isinstance(item, FieldInfo) for item in expands.values()
    ), "Invalid value type in 'expands' dict"


@pytest.mark.parametrize(
    "pipeline_job",
    list_pipeline_job_cls(),
)
def test_pipeline_job_basics(
    pipeline_job: type[_PipelineJob],
) -> None:
    """Test pipeline jobs."""
    # enpoint subclass
    assert issubclass(
        pipeline_job,
        Endpoint,
    ), "pipeline job is not a subclass of '_Endpoint'"
    assert issubclass(
        pipeline_job,
        _PipelineJob,
    ), "pipeline job is not a subclass of '_PipelineJob'"

    # command
    assert (
        "command" in pipeline_job.model_fields
    ), "pipeline job does not have attribute 'command'"
    command: FieldInfo = pipeline_job.model_fields["command"]
    assert command.default in ("PipelineRun", "Import", "XMLImport"), "Invalid command"


def test_resource_model() -> None:
    """Test resource models."""

    class DummyResource(Resource):
        """Dummy resource model."""

        attr_seq: ClassVar[str] = "dummy_seq"
        dummy_seq: str | None = None
        name: str
        dummy_int: int

    dummy_data: dict[str, Any] = {
        "dummySeq": "spam",
        "name": "eggs",
        "dummyInt": 42,
        "extraField": {"spam": "eggs"},
    }

    dummy_resource: DummyResource = DummyResource(**dummy_data)
    assert dummy_resource.dummy_seq == "spam"
    assert dummy_resource.name == "eggs"
    assert dummy_resource.dummy_int == 42

    dump: dict[str, Any] = dummy_resource.model_dump(by_alias=True, exclude_none=True)
    assert dump == dummy_data

    extra: dict[str, Any] | None = dummy_resource.model_extra
    assert extra is not None
    # pylint: disable=unsupported-membership-test
    assert "dummySeq" not in extra
    assert "name" not in extra
    assert "dummyInt" not in extra
    assert "extraField" in extra
    # pylint: disable=unsubscriptable-object
    assert extra["extraField"] == {"spam": "eggs"}


def test_model_alias_override() -> None:
    """Test model alias override."""

    class DummyResource(Resource):
        """Dummy model."""

        dummy_code_id: str = Field(
            validation_alias=AliasChoices("dummyCodeId", "ID"),
        )

    data: dict[str, str] = {"dummyCodeId": "spam"}
    dummy: DummyResource = DummyResource(**data)  # type: ignore[arg-type]
    assert dummy.dummy_code_id == "spam"
    dump: dict[str, str] = dummy.model_dump(by_alias=True, exclude_none=True)
    assert dump == data

    data2: dict[str, str] = {"ID": "eggs"}
    dummy2: DummyResource = DummyResource(**data2)  # type: ignore[arg-type]
    assert dummy2.dummy_code_id == "eggs"
    dump2: dict[str, str] = dummy2.model_dump(by_alias=True, exclude_none=True)
    assert "ID" not in dump2


@pytest.mark.parametrize(
    "resource_cls",
    list_resource_cls(),
)
def test_resource_reference(
    resource_cls: type[Resource],
) -> None:
    """Test resource reference."""
    data: dict[str, Any] = {
        "key": "spam",
        "displayName": "eggs",
        "objectType": resource_cls.__name__,
        "logicalKeys": {"name": "eggs"},
    }
    reference: Reference = Reference(**data)
    assert reference.key == "spam"
    assert reference.display_name == "eggs"
    assert reference.object_type is resource_cls


def test_resource_reference_error() -> None:
    """Test resource reference."""
    data1: dict[str, Any] = {
        "key": "spam",
        "displayName": "eggs",
        "objectType": "Bacon",
        "logicalKeys": {"name": "eggs"},
    }
    with pytest.raises(ValueError) as exc:
        Reference(**data1)
        assert "Unknown object type" in str(exc)

    data2: dict[str, Any] = {
        "key": "spam",
        "displayName": "eggs",
        "objectType": "Value",
        "logicalKeys": {"name": "eggs"},
    }
    with pytest.raises(ValueError) as exc:
        Reference(**data2)
        assert "Invalid object type" in str(exc)


def test_reference_string() -> None:
    """Test reference field as string."""

    class DummyResource(Resource):
        """Dummy model."""

        id: str
        reference: str | Reference

    data: dict[str, str] = {"id": "spamm", "reference": "eggs"}
    dummy: DummyResource = DummyResource(**data)  # type: ignore[arg-type]
    assert dummy.id == "spamm"
    assert isinstance(dummy.reference, str)
    assert dummy.reference == "eggs"

    data2: dict[str, str | dict[str, Any]] = {
        "id": "spamm",
        "reference": {
            "key": "eggs",
            "displayName": "Eggs",
            "objectType": "User",
            "logicalKeys": {"likes": "bacon"},
        },
    }
    dummy2: DummyResource = DummyResource(**data2)  # type: ignore[arg-type]
    assert dummy2.id == "spamm"
    assert isinstance(dummy2.reference, Reference)
    assert str(dummy2.reference) == "eggs"
    assert issubclass(dummy2.reference.object_type, Resource)

    assert isinstance(dummy2.reference.logical_keys, dict)
    logical_keys: dict[str, Any] = dummy2.reference.logical_keys
    assert logical_keys["likes"] == "bacon"
