"""Test for SAP Commissions Models."""
# pylint: disable=protected-access

import logging
from collections.abc import Generator
from inspect import isclass
from typing import Any, ClassVar, TypeVar

import pytest
from pydantic import AliasChoices, BaseModel, Field
from pydantic.fields import FieldInfo

from sapcommissions import model

LOGGER: logging.Logger = logging.getLogger(__name__)
T = TypeVar("T", bound="model._Endpoint")
U = TypeVar("U", bound="model._Resource")
V = TypeVar("V", bound="model._PipelineJob")


def list_endpoint_cls() -> Generator[type[model._Endpoint], None, None]:
    """List all endpoint classes in the model module."""
    for name in dir(model):
        obj = getattr(model, name)
        if (
            isclass(obj)
            and issubclass(obj, model._Endpoint)
            and not obj.__name__.startswith("_")
        ):
            yield obj


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


def list_pipeline_job_cls() -> Generator[type[model._PipelineJob], None, None]:
    """List all pipeline job classes in the model module."""
    for name in dir(model):
        obj = getattr(model, name)
        if (
            isclass(obj)
            and issubclass(obj, model._PipelineJob)
            and not obj.__name__.startswith("_")
        ):
            yield obj


@pytest.mark.parametrize(
    "endpoint_cls",
    list_endpoint_cls(),
)
def test_endpoint_basics(
    endpoint_cls: type[T],
) -> None:
    """Test endpoints."""
    assert issubclass(
        endpoint_cls,
        BaseModel,
    ), "endpoint is not a pydantic model"
    assert issubclass(
        endpoint_cls,
        model._BaseModel,
    ), "endpoint is not a subclass of '_BaseModel'"
    assert issubclass(
        endpoint_cls,
        model._Endpoint,
    ), "endpoint is not a subclass of '_Endpoint'"

    # _endpoint
    assert hasattr(
        endpoint_cls,
        "_endpoint",
    ), "resource does not have attribute '_endpoint'"
    endpoint: str = endpoint_cls._endpoint
    assert endpoint.startswith("api/v2/"), "_endpoint should start with 'api/v2/'"


@pytest.mark.parametrize(
    "resource_cls",
    list_resource_cls(),
)
def test_resource_basics(
    resource_cls: type[U],
) -> None:
    """Test resources."""
    # enpoint subclass
    assert issubclass(
        resource_cls,
        model._Endpoint,
    ), "resource is not a subclass of '_Endpoint'"

    # _attr_seq
    assert hasattr(
        resource_cls,
        "_attr_seq",
    ), "resource does not have attribute '_attr_seq'"
    attr_seq: str = resource_cls._attr_seq
    assert attr_seq.endswith("_seq"), "_attr_seq should end with '_seq'"

    # seq field
    assert attr_seq in resource_cls.model_fields
    seq_field: FieldInfo = resource_cls.model_fields[attr_seq]
    assert seq_field.annotation == str | None
    assert seq_field.default is None


@pytest.mark.parametrize(
    "pipeline_job",
    list_pipeline_job_cls(),
)
def test_pipeline_job_basics(
    pipeline_job: type[V],
) -> None:
    """Test pipeline jobs."""
    # enpoint subclass
    assert issubclass(
        pipeline_job,
        model._Endpoint,
    ), "pipeline job is not a subclass of '_Endpoint'"

    # command
    assert (
        "command" in pipeline_job.model_fields
    ), "pipeline job does not have attribute 'command'"
    command: FieldInfo = pipeline_job.model_fields["command"]
    assert command.default in ("PipelineRun", "Import", "XMLImport"), "Invalid command"


def test_resource_model() -> None:
    """Test resource models."""

    class DummyResource(model._Resource):
        """Dummy resource model."""

        _attr_seq: ClassVar[str] = "dummy_seq"
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
    LOGGER.info("Resource: %s", dummy_resource)
    assert dummy_resource.dummy_seq == "spam"
    assert dummy_resource.name == "eggs"
    assert dummy_resource.dummy_int == 42

    dump: dict[str, Any] = dummy_resource.model_dump(by_alias=True, exclude_none=True)
    LOGGER.info("Dump: %s", dump)
    assert dump == dummy_data

    extra: dict[str, Any] | None = dummy_resource.model_extra
    assert extra is not None
    LOGGER.info("Extra: %s", extra)
    # pylint: disable=unsupported-membership-test
    assert "dummySeq" not in extra
    assert "name" not in extra
    assert "dummyInt" not in extra
    assert "extraField" in extra
    # pylint: disable=unsubscriptable-object
    assert extra["extraField"] == {"spam": "eggs"}


def test_model_alias_override() -> None:
    """Test model alias override."""

    class DummyResource(model._Resource):
        """Dummy model."""

        dummy_code_id: str = Field(
            validation_alias=AliasChoices("dummyCodeId", "ID"),
        )

    data: dict[str, str] = {"dummyCodeId": "spam"}
    dummy: DummyResource = DummyResource(**data)  # type: ignore[arg-type]
    assert dummy.dummy_code_id == "spam"
    dump: dict[str, str] = dummy.model_dump(by_alias=True, exclude_none=True)
    assert dump == data
