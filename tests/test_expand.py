"""Test the resource expand feature."""
# pylint: disable=protected-access

import logging
import warnings
from typing import TypeVar

from sapcommissions import CommissionsClient, model
from sapcommissions.helpers import get_alias

LOGGER = logging.getLogger(__name__)
T = TypeVar("T", bound=model.base.Resource)
warnings.filterwarnings("error")  # Raise warnings as errors


async def test_expand_credit(client: CommissionsClient) -> None:
    """Test expand Credit."""
    LOGGER.info("Testing expand on Credit")

    resource_cls = model.Credit
    expand_fields = resource_cls.expands()
    expand_alias = [get_alias(resource_cls, field_name) for field_name in expand_fields]
    expand = ",".join(expand_alias)
    params: dict[str, int | str] = {
        "top": 1,
        "expand": expand,
    }

    raw_data = await client._request("GET", resource_cls.attr_endpoint, params=params)
    first_key: str = list(raw_data.keys())[0]
    LOGGER.info("First key: %s", first_key)
    raw_resource = raw_data[first_key][0]
    for field_name in expand_alias:
        LOGGER.info("%s: %s", field_name, raw_resource.get(field_name, None))

    resource = await client.read_first(resource_cls)
    assert isinstance(resource, resource_cls)

    LOGGER.info("Resource: %s", resource)
    for field_name in expand_fields:
        LOGGER.info("%s: %s", field_name, getattr(resource, field_name))


async def test_expand_sales_transaction(client: CommissionsClient) -> None:
    """Test expand SalesTransaction."""
    LOGGER.info("Testing expand on SalesTransaction")

    resource_cls = model.SalesTransaction
    expand_fields = resource_cls.expands()
    expand_alias = [get_alias(resource_cls, field_name) for field_name in expand_fields]
    expand = ",".join(expand_alias)
    params: dict[str, int | str] = {
        "top": 1,
        "expand": expand,
    }

    raw_data = await client._request("GET", resource_cls.attr_endpoint, params=params)
    first_key: str = list(raw_data.keys())[0]
    LOGGER.info("First key: %s", first_key)
    raw_resource = raw_data[first_key][0]
    for field_name in expand_alias:
        LOGGER.info("%s: %s", field_name, raw_resource.get(field_name, None))

    resource = await client.read_first(resource_cls)
    assert isinstance(resource, resource_cls)

    LOGGER.info("Resource: %s", resource)
    for field_name in expand_fields:
        LOGGER.info("%s: %s", field_name, getattr(resource, field_name))
