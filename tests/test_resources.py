"""Test the resource interaction with the client."""
# pylint: disable=protected-access

import logging
import warnings
from json import dumps
from typing import Any, TypeVar

import pytest

from sapcommissions import CommissionsClient, model
from sapcommissions.helpers import AsyncLimitedGenerator
from sapcommissions.model.base import Reference, Resource

from tests.conftest import list_resource_cls

LOGGER = logging.getLogger(__name__)
T = TypeVar("T", bound=model.base.Resource)
warnings.filterwarnings("error")  # Raise warnings as errors


pytest.skip("These tests perform requests on your tenant", allow_module_level=True)


@pytest.mark.parametrize(
    "resource_cls",
    list_resource_cls(),
)
async def test_list_resources(  # noqa: C901
    client: CommissionsClient,
    resource_cls: type[T],
) -> None:
    """Test listing resources."""
    LOGGER.info("Testing list %s", resource_cls.__name__)

    resource_list: list[T] = []

    page_size: int = (
        1 if resource_cls is model.SalesTransaction else 100
    )  # FIX Issue #30
    generator = client.read_all(resource_cls, page_size=page_size)
    async for resource in AsyncLimitedGenerator(generator, page_size * 2):
        assert isinstance(resource, resource_cls)
        resource_list.append(resource)

    if not resource_list:
        pytest.skip("No resources found")

    extra_keys: dict[str, set[Any]] = {}
    for instance in resource_list:
        if model_extra := instance.model_extra:
            model_extra.pop("etag", None)
            for key, value in model_extra.items():
                extra_keys.setdefault(key, set())
                extra_keys[key].add(str(value))

    LOGGER.info("Extra keys: %s", extra_keys)
    assert not extra_keys, f"Extra keys: {extra_keys}"


@pytest.mark.parametrize(
    "resource_cls",
    list_resource_cls(),
)
async def test_model_raw(
    client: CommissionsClient,
    resource_cls: type[T],
) -> None:
    """Test the raw model."""
    LOGGER.info("Testing raw model %s", resource_cls.__name__)

    params: dict[str, int | str] = {"top": 1}
    expand_fields = resource_cls.expands()
    assert expand_fields, "Resource does not expand any fields."
    expand_alias = [
        field_info.alias for field_info in expand_fields.values() if field_info.alias
    ]
    assert expand_alias, "Expand fields do not have any alias."
    if expand := ",".join(expand_alias):
        params["expand"] = expand

    LOGGER.info("Params: %s", params)
    data = await client._request("GET", resource_cls.attr_endpoint, params=params)
    LOGGER.info("Data: %s", dumps(data, indent=2))


@pytest.mark.parametrize(
    "resource_cls",
    list_resource_cls(),
)
async def test_expand_resources(  # noqa: C901
    client: CommissionsClient,
    resource_cls: type[T],
) -> None:
    """Test listing resources."""
    LOGGER.info("Testing list %s", resource_cls.__name__)

    resource_list: list[T] = []

    page_size: int = (
        1 if resource_cls is model.SalesTransaction else 100
    )  # FIX Issue #30
    generator = client.read_all(resource_cls, page_size=page_size)
    async for resource in AsyncLimitedGenerator(generator, page_size * 2):
        assert isinstance(resource, resource_cls)
        resource_list.append(resource)

    if not resource_list:
        pytest.skip("No resources found")

    for resource in resource_list:
        expand_fields = resource_cls.expands()
        if not expand_fields:
            pytest.skip("Resource does not expand any fields.")

        for field_name in expand_fields:
            if field_value := getattr(resource, field_name):
                assert isinstance(
                    field_value, Reference
                ), f"{field_name}: Invalid Reference '{field_value}'."
                assert issubclass(
                    field_value.object_type, Resource
                ), f"{field_name}: Invalid reference type '{field_value.object_type}'."
