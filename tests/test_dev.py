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

LOGGER: logging.Logger = logging.getLogger(__name__)


async def test_endpoint_response(client_dev: CommissionsClient) -> None:
    """Perform list operation on an endpoint and analyse result."""
    limit: int = 1000
    cls = model.Credit
    items_list = client_dev.read_all(
        cls,
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
        for k, v in item.items():
            dict_of_list.setdefault(k, [])
            dict_of_list[k].append(v)

    empty_fields: set[str] = set()
    none_empty_fields: set[str] = set()
    unique_values: dict[str, set] = {}
    unmapped_fields: set[str] = set()

    for k1, v1 in dict_of_list.items():
        if k1 not in cls.model_fields and k1 != "etag":
            if k1 not in [
                info.alias for info in cls.model_fields.values() if info.alias
            ]:
                unmapped_fields.add(k1)
        if all(value is None for value in v1):
            empty_fields.add(k1)
        if all(value is not None for value in v1) and k1 != "etag":
            none_empty_fields.add(k1)
        try:
            if len(set(v1)) < len(v1):
                unique_values.setdefault(k1, set())
                unique_values[k1].update(v1)
        except TypeError:
            # LOGGER.debug(f"{key=}, {values=}")
            try:
                for lst in v1:
                    unique_values.setdefault(k1, set())
                    unique_values[k1].update(lst)
            except TypeError:
                LOGGER.info(f"unique_values for {k1}: {v1}")

    LOGGER.info(cls.__name__)
    LOGGER.info(f"fields={set(dict_of_list.keys())}")
    LOGGER.info(f"{empty_fields=}")
    LOGGER.info(f"{none_empty_fields=}")
    LOGGER.info(f"{unmapped_fields=}")
    for k2, v2 in unique_values.items():
        if k2 in unmapped_fields and k2 != "etag":
            LOGGER.info(f"unique_values for {k2}: {v2}")

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
    for k1, v1 in validation_errors.items():
        LOGGER.error(f"validation_errors for {k1}: {v1}")


if __name__ == "__main__":
    pytest.main([__file__])
