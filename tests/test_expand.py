"""Test the resource expand feature."""
# pylint: disable=protected-access

import logging
import warnings
from json import dumps
from typing import TypeVar

from sapcommissions import CommissionsClient, model
from sapcommissions.helpers import get_alias

LOGGER = logging.getLogger(__name__)
T = TypeVar("T", bound=model.base.Resource)
warnings.filterwarnings("error")  # Raise warnings as errors


async def test_expand_credits(client: CommissionsClient) -> None:
    """Test expanding credits."""
    LOGGER.info("Testing expand on Credits")

    expand = ",".join(model.Credit.attr_expand)
    params: dict[str, int | str] = {"top": 1}
    if expand:
        params["expand"] = expand
    LOGGER.info("Params: %s", params)

    raw_data = await client._request("GET", model.Credit.attr_endpoint, params=params)
    LOGGER.info("Data: %s", dumps(raw_data, indent=2))

    raw_credit = raw_data["credits"][0]
    for field in model.Credit.attr_expand:
        LOGGER.info("%s: %s", field, raw_credit.get(field, None))

    credit = await client.read_first(model.Credit)
    assert isinstance(credit, model.Credit)

    LOGGER.info("Credit: %s", credit)
    for field in model.Credit.attr_expand:
        LOGGER.info("%s: %s", field, field)


async def test_expand_alias() -> None:
    """Testing field alias."""

    expand = model.Credit.attr_expand
    LOGGER.info("Expands: %s", expand)

    aliases = {
        field_name: get_alias(model.Credit, field_name)
        for field_name in model.Credit.attr_expand
    }
    LOGGER.info("%s aliases: %s", model.Credit.__name__, aliases)
