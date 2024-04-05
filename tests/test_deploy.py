"""Test the deployment module."""

import logging
from pathlib import Path

from aiohttp import ClientSession

from sapcommissions import CommissionsClient, deploy

LOGGER: logging.Logger = logging.getLogger(__name__)


async def test_deploy_from_path(
    config: dict[str, str],
    session: ClientSession,
) -> None:
    """Test the deploy_from_path function."""
    path: Path = Path("tests/deploy")
    client = CommissionsClient(
        tenant=config["SAP_TENANT"],
        session=session,
        verify_ssl=False,
    )
    result = await deploy.deploy_from_path(client, path)
    LOGGER.info(result)
