"""Test the resource interaction with the Tenant."""
# pylint: disable=protected-access

import logging
import warnings
from typing import Any, TypeVar

import pytest

from sapimclient import Tenant, model
from sapimclient.helpers import AsyncLimitedGenerator
from sapimclient.model.base import Reference, Resource

from tests.conftest import list_resource_cls

LOGGER = logging.getLogger(__name__)
T = TypeVar('T', bound=model.base.Resource)
warnings.filterwarnings('error')  # Raise warnings as errors


@pytest.mark.parametrize(
    'resource_cls',
    list_resource_cls(),
)
async def test_resource_model(
    live_tenant: Tenant,
    resource_cls: type[T],
) -> None:
    """Test resource model is complete."""
    LOGGER.info('Testing list %s', resource_cls.__name__)

    resource_list: list[T] = []

    page_size: int = (
        1 if resource_cls is model.SalesTransaction else 100
    )  # FIX Issue #30
    generator = live_tenant.read_all(resource_cls, page_size=page_size)
    async for resource in AsyncLimitedGenerator(generator, page_size * 2):
        assert isinstance(resource, resource_cls)
        resource_list.append(resource)

    if not resource_list:
        pytest.skip('No resources found')

    extra_keys: dict[str, set[Any]] = {}
    for instance in resource_list:
        if model_extra := instance.model_extra:
            model_extra.pop('etag', None)  # etag is allowed as extra field
            for key, value in model_extra.items():
                extra_keys.setdefault(key, set())
                extra_keys[key].add(str(value))

    if extra_keys:
        pytest.fail(f'Extra keys found: {extra_keys}')


@pytest.mark.parametrize(
    'resource_cls',
    list_resource_cls(),
)
async def test_resource_reference(
    live_tenant: Tenant,
    resource_cls: type[T],
) -> None:
    """Test resource expanded fields are reference objects to existing resource."""
    LOGGER.info('Testing list %s', resource_cls.__name__)

    resource_list: list[T] = []

    page_size: int = (
        1 if resource_cls is model.SalesTransaction else 100
    )  # FIX Issue #30
    generator = live_tenant.read_all(resource_cls, page_size=page_size)
    async for resource in AsyncLimitedGenerator(generator, page_size * 2):
        assert isinstance(resource, resource_cls)
        resource_list.append(resource)

    if not resource_list:
        pytest.skip('No resources found')

    for resource in resource_list:
        if not (expand_fields := resource_cls.expands()):
            pytest.skip('Resource does not expand any fields.')

        for field_name in expand_fields:
            if field_value := getattr(resource, field_name):
                assert isinstance(
                    field_value,
                    Reference,
                ), f"{field_name}: Invalid Reference '{field_value}'."
                assert issubclass(
                    field_value.object_type,
                    Resource,
                ), f"{field_name}: Invalid reference type '{field_value.object_type}'."
