"""Test the resource interaction with the client."""
# pylint: disable=protected-access

import logging
import warnings
from typing import Any, TypeVar

import pytest

from sapcommissions import CommissionsClient, model
from tests.conftest import AsyncLimitedGenerator, list_resource_cls

LOGGER = logging.getLogger(__name__)
T = TypeVar("T", bound=model._Resource)
warnings.filterwarnings("error")  # Raise warnings as errors


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
    extra: dict[str, set[Any]] = {}

    generator = client.read_all(resource_cls, page_size=100)
    async for resource in AsyncLimitedGenerator(generator, 100):
        assert isinstance(resource, resource_cls)
        resource_list.append(resource)

    if not resource_list:
        pytest.skip("No resources found")

    LOGGER.info("Resource example: %s", resource_list[-1])
    for instance in resource_list:
        if model_extra := instance.model_extra:
            for key, value in model_extra.items():
                if key not in ("etag",):
                    if key not in extra:
                        extra[key] = set()
                    try:
                        extra[key].add(value)
                    except TypeError:
                        extra[key].add(str(value))

    LOGGER.info("Extra keys: %s", extra)
    assert not extra, f"Extra keys: {extra}"
