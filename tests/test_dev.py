"""Some tests for development."""
# ruff: noqa
# pylint: disable-all

import asyncio
import logging
from collections.abc import AsyncGenerator
from datetime import date
from typing import Any

import pytest
from pydantic import ValidationError

from sapcommissions import CommissionsClient, model
from sapcommissions.helpers import And, Equals, GreaterThenOrEqual

LOGGER = logging.getLogger(__name__)


async def test_endpoint_response(client_dev: CommissionsClient) -> None:
    """Perform list operation on an endpoint and analyse result."""
    limit: int = 1000
    cls = model.Credit
    items_list: AsyncGenerator[dict[str, Any], None] = client_dev.list(
        cls,
        raw=True,
        page_size=100,
    )

    i: int = 0
    items: list[dict[str, Any]] = []
    async for item in items_list:
        i += 1
        items.append(item)
        if i > limit:
            break

    dict_of_list: dict[str, list[Any]] = {}
    for item in items:
        # LOGGER.info(item)
        for key, value in item.items():
            dict_of_list.setdefault(key, [])
            dict_of_list[key].append(value)

    empty_fields: set[str] = set()
    none_empty_fields: set[str] = set()
    unique_values: dict[str, set] = {}
    unmapped_fields: set[str] = set()

    for key, values in dict_of_list.items():
        if key not in cls.model_fields and key != "etag":
            if key not in [
                info.alias for info in cls.model_fields.values() if info.alias
            ]:
                unmapped_fields.add(key)
        if all(value is None for value in values):
            empty_fields.add(key)
        if all(value is not None for value in values) and key != "etag":
            none_empty_fields.add(key)
        try:
            if len(set(values)) < len(values):
                unique_values.setdefault(key, set())
                unique_values[key].update(values)
        except TypeError:
            # LOGGER.debug(f"{key=}, {values=}")
            try:
                for lst in values:
                    unique_values.setdefault(key, set())
                    unique_values[key].update(lst)
            except TypeError:
                LOGGER.info(f"unique_values for {key}: {values}")

    LOGGER.info(cls.__name__)
    LOGGER.info(f"fields={set(dict_of_list.keys())}")
    LOGGER.info(f"{empty_fields=}")
    LOGGER.info(f"{none_empty_fields=}")
    LOGGER.info(f"{unmapped_fields=}")
    for key, values in unique_values.items():
        if key in unmapped_fields and key != "etag":
            LOGGER.info(f"unique_values for {key}: {values}")

    # Test for validation errors
    validation_errors: dict[str, set[str]] = {}
    for item in items:
        try:
            # LOGGER.info(cls(**item))
            cls(**item)
        except ValidationError as exc:
            errors = exc.errors()
            for error in errors:
                LOGGER.debug(error)
                loc = error["loc"][0]
                msg = error["msg"]
                input = error["input"]
                validation_errors.setdefault(loc, set())
                validation_errors[loc].add(f"{input}: {msg}")
    for key, values in validation_errors.items():
        LOGGER.error(f"validation_errors for {key}: {values}")


if __name__ == "__main__":
    pytest.main([__file__])
