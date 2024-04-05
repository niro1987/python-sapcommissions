"""Test the deployment module."""

import logging
from pathlib import Path

from aiohttp import BasicAuth, ClientSession
from dotenv import dotenv_values

from sapcommissions import CommissionsClient, deploy

LOGGER = logging.getLogger(__name__)


async def test_deploy_from_path() -> None:
    """Test the deploy_from_path function."""
    config: dict[str, str] = dotenv_values("tests/.env")
    auth: BasicAuth = BasicAuth(
        login=config["SAP_USERNAME"],
        password=config["SAP_PASSWORD"],
    )
    path: Path = Path("tests/deploy")

    async with ClientSession(auth=auth) as session:
        client = CommissionsClient(
            tenant=config["SAP_TENANT"],
            session=session,
            verify_ssl=False,
        )
        result = await deploy.deploy_from_path(client, path)
        LOGGER.info(result)
