"""CLI entry point for Python SAP Commissions Client."""

import asyncio
import logging
import os
import sys
from logging.config import dictConfig
from pathlib import Path

import click
from aiohttp import BasicAuth, ClientSession

from sapcommissions import CommissionsClient
from sapcommissions.deploy import deploy_from_path

LOGGER: logging.Logger = logging.getLogger(__package__)


def setup_logging(logfile: Path | None = None, verbose: bool = False) -> None:
    """Set up logging and add filehandler if logfile is provided."""
    config = {
        "version": 1,
        "formatters": {
            "standard": {
                "format": "%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
    }
    handlers = {
        "console": {"class": "logging.StreamHandler", "formatter": "standard"},
    }
    if logfile:
        handlers["file"] = {
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": str(str(logfile)),
        }
    loggers = {
        __package__: {
            "handlers": list(handlers.keys()),
            "level": "DEBUG" if verbose else "INFO",
        },
    }
    config["handlers"] = handlers
    config["loggers"] = loggers
    dictConfig(config)


async def async_deploy(
    path: Path,
    tenant: str,
    auth: BasicAuth,
    verify_ssl: bool = True,
) -> int:
    """Deploy rule elements asynchronously from a directory to the tenant.

    Args:
    ----
        path (Path): The path to the directory containing the rule elements.
        tenant (str): The tenant to deploy the rule elements to.
        auth (BasicAuth): The authentication credentials for the tenant.
        verify_ssl (bool, optional): Whether to verify SSL certificates. Defaults to True.

    Returns:
    -------
        int: The result of the deployment process.

    """
    async with ClientSession(auth=auth) as session:
        client = CommissionsClient(tenant, session, verify_ssl)
        await deploy_from_path(client, path)
    return 0


@click.group()
@click.option(
    "-l",
    "--logfile",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        resolve_path=False,
        path_type=Path,
    ),
    help="Enable logging to a file.",
)
@click.option("-v", is_flag=True, help="Increase logging verbosity.")
def cli(logfile: Path | None = None, v: bool = False) -> None:
    """Command-line interface for sapcommissions."""
    setup_logging(logfile, v)
    LOGGER.info("sapcommissions command-line interface")


@cli.command()
@click.argument(
    "path",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=False,
        path_type=Path,
    ),
)
@click.option("-t", "--tenant", type=str, help="Tenant, for example `CALD-DEV`.")
@click.option("-u", "--username", type=str, help="Username for tenant.")
@click.option("-p", "--password", type=str, help="Password for tenant.")
@click.option("--no-ssl", is_flag=True, help="Disable SSL validation.")
def deploy(
    path: Path,
    tenant: str | None = None,
    username: str | None = None,
    password: str | None = None,
    no_ssl: bool = False,
):
    """Deploy rule elements from a directory to the tenant.

    Args:
    ----
        path (Path): The path to the directory containing the rule elements.
        tenant (str, optional): The tenant to deploy the rule elements to. Defaults to None.
        username (str, optional): The username for the tenant. Defaults to None.
        password (str, optional): The password for the tenant. Defaults to None.
        no_ssl (bool, optional): Whether to disable SSL validation. Defaults to False.

    Returns:
    -------
        int: The result of the deployment process.

    """
    sap_tenant: str | None = tenant or os.environ.get("SAP_TENANT")
    sap_username: str | None = username or os.environ.get("SAP_USERNAME")
    sap_password: str | None = password or os.environ.get("SAP_PASSWORD")
    if not (sap_tenant and sap_username and sap_password):
        LOGGER.error("Tenant, Username or password not set")
        return 1
    LOGGER.info("deploy '%s' on '%s' by '%s'", path, sap_tenant, sap_username)
    auth = BasicAuth(sap_username, sap_password)

    if no_ssl:
        LOGGER.info("SSL validation disabled")
    verify_ssl = not no_ssl

    asyncio.run(async_deploy(path, sap_tenant, auth, verify_ssl))
    return 0


if __name__ == "__main__":
    sys.exit(cli())
