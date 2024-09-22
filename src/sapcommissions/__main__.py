"""CLI entry point for Python SAP Commissions Client."""
# pylint: disable=too-many-arguments, no-value-for-parameter

import asyncio
import logging
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
    """Async deploy rule elements from a directory to the tenant."""
    async with ClientSession(auth=auth) as session:
        client = CommissionsClient(tenant, session, verify_ssl)
        await deploy_from_path(client, path)
    return 0


@click.group()
@click.pass_context
@click.option(
    "-t",
    "--tenant",
    prompt=True,
    help="Tenant to connect to, for example 'CALD-DEV'.",
)
@click.option(
    "-u",
    "--username",
    prompt=True,
    help="Username for authentication.",
)
@click.option(
    "-p",
    "--password",
    prompt=True,
    hide_input=True,
    help="Password for authentication.",
)
@click.option(
    "--no-ssl",
    is_flag=True,
    help="Disable SSL validation.",
)
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
@click.option(
    "-v",
    is_flag=True,
    help="Increase logging verbosity.",
)
def cli(  # noqa: PLR0913
    ctx: click.Context,
    tenant: str,
    username: str,
    password: str,
    no_ssl: bool = False,
    logfile: Path | None = None,
    v: bool = False,
) -> None:
    """Command-line interface for Python SAP Commissions.

    You may provide parameters by setting environment variables prefixed with 'SAP_' or
    by passing them as options. For example: `export SAP_TENANT=CALD-DEV` is equivalent
    to passing `--tenant CALD-DEV`

    """
    ctx.ensure_object(dict)
    ctx.obj["TENANT"] = tenant
    ctx.obj["USERNAME"] = username
    ctx.obj["PASSWORD"] = password
    ctx.obj["SSL"] = not no_ssl

    setup_logging(logfile, v)


@cli.command()
@click.pass_context
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
def deploy(
    ctx: click.Context,
    path: Path,
):
    """Deploy rule elements from a directory to the tenant."""

    tenant: str = ctx.obj["TENANT"]
    username: str = ctx.obj["USERNAME"]
    password: str = ctx.obj["PASSWORD"]
    ssl: bool = ctx.obj["SSL"]

    LOGGER.info("deploy '%s' on '%s'", path, tenant)
    auth = BasicAuth(username, password)

    if not ssl:
        LOGGER.info("SSL validation disabled")

    asyncio.run(async_deploy(path, tenant, auth, ssl))
    return 0


if __name__ == "__main__":
    sys.exit(cli(obj={}, auto_envvar_prefix="SAP"))
