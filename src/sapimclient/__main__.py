"""CLI entry point for Python SAP Incentive Management Client."""

import asyncio
import logging
import sys
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from logging.config import dictConfig
from pathlib import Path
from typing import Any

import click
from aiohttp import BasicAuth, ClientSession

from sapimclient import Tenant, export as sap_export, helpers, model
from sapimclient.deploy import deploy_from_path
from sapimclient.exceptions import SAPNotFoundError

LOGGER: logging.Logger = logging.getLogger(__name__)


class DynamicChoice(click.ParamType):
    """Class to enable dynamic choise."""

    def __init__(self, name: str, choices_getter: Callable) -> None:
        """Initialize DynamicChoise."""
        self.name = name
        self.choices_getter = choices_getter

    def convert(
        self,
        value: Any,
        param: click.Parameter | None = None,
        ctx: click.Context | None = None,
    ) -> Any:
        """Validate and Convert Value."""
        choices = self.choices_getter(ctx)
        if value not in choices:
            self.fail(
                f'{value} is not a valid choice. Choose from: {choices}.',
                param,
                ctx,
            )
        return value


def setup_logging(
    *,
    filename: Path | None = None,
    verbose: bool = False,
    debug: bool = False,
) -> None:
    """Set up logging."""
    config = {
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
    }
    handlers = {}
    if verbose:
        handlers['console'] = {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }
    if filename:
        handlers['file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': str(str(filename)),
        }
    loggers = {
        __package__: {
            'handlers': list(handlers.keys()),
            'level': 'DEBUG' if debug else 'INFO',
        },
    }
    config['handlers'] = handlers
    config['loggers'] = loggers
    dictConfig(config)


@asynccontextmanager
async def session_client(ctx: click.Context) -> AsyncGenerator[Tenant, None]:
    """Yield a Session enabled Tenant."""
    tenant: str = ctx.obj['TENANT']
    username: str = ctx.obj['USERNAME']
    password: str = ctx.obj['PASSWORD']
    ssl: bool = ctx.obj['SSL']
    auth = BasicAuth(username, password)
    async with ClientSession(auth=auth) as session:
        client: Tenant = Tenant(
            tenant=tenant,
            session=session,
            verify_ssl=ssl,
            request_timeout=60,
        )
        yield client
        LOGGER.debug('Closed session.')


async def async_deploy(path: Path, ctx: click.Context) -> None:
    """Async deploy rule elements from a directory to the tenant."""
    async with session_client(ctx) as client:
        await deploy_from_path(client, path)


async def async_list_calendars(ctx: click.Context) -> list[str]:
    """Async list all calendars."""
    calendar_names: list[str] = []
    async with session_client(ctx) as client:
        generator = client.read_all(model.Calendar)
        calendar_names.extend([item.name async for item in generator])
    return calendar_names


def list_calendars(ctx: click.Context) -> list[str]:
    """List all calendars."""
    return asyncio.run(async_list_calendars(ctx))


async def async_list_periods(
    ctx: click.Context,
    calendar_name: str,
    period_name: str | None = None,
) -> list[str]:
    """Async list all periods for a calendar."""
    period_names: list[str] = []

    async with session_client(ctx) as client:
        calendar_obj: model.Calendar | None = await client.read_first(
            model.Calendar,
            filters=helpers.Equals('name', calendar_name),
        )
        if not calendar_obj:
            raise SAPNotFoundError('Calendar')
        filters = [
            helpers.Equals('calendar', str(calendar_obj.seq)),
            helpers.Equals('periodType', str(calendar_obj.minor_period_type)),
        ]
        if period_name is not None:
            filters.append(helpers.Equals('name', period_name))
        generator = client.read_all(
            model.Period,
            filters=helpers.And(*filters),
            order_by=['startDate desc'],
        )
        period_names.extend([item.name async for item in generator])
    return period_names


def list_periods(
    ctx: click.Context,
    calendar_name: str,
    period_name: str | None = None,
) -> list[str]:
    """List all calendars."""
    return asyncio.run(async_list_periods(ctx, calendar_name, period_name))


def validate_period(ctx: click.Context, _: click.Parameter | None, value: Any) -> Any:
    """Validate the Period input."""
    if value is None:
        return None
    if not (calendar_name := ctx.params.get('calendar', None)):
        raise click.BadParameter(message='Must provide Calendar before Period.')
    period_names = list_periods(
        ctx=ctx,
        calendar_name=calendar_name,
        period_name=value,
    )
    if value not in period_names:
        raise click.BadParameter(message=f"Period does not exist in '{calendar_name}'.")
    return value


async def async_load_resource(
    ctx: click.Context,
    resource: str,
    path: Path,
    filters: str | None = None,
) -> None:
    """Load Credits report to file."""
    async with session_client(ctx) as client:
        if resource == 'CREDITS':
            await sap_export.load_credits(client, filters, path)
        elif resource == 'MEASUREMENTS':
            await sap_export.load_measurements(client, filters, path)
        elif resource == 'INCENTIVES':
            await sap_export.load_incentives(client, filters, path)
        elif resource == 'COMMISSIONS':
            await sap_export.load_commissions(client, filters, path)
        elif resource == 'DEPOSITS':
            await sap_export.load_deposits(client, filters, path)
        elif resource == 'PAYMENTS':
            await sap_export.load_payment_summary(client, filters, path)


@click.group()
@click.pass_context
@click.option(
    '-t',
    '--tenant',
    prompt=True,
    help="Tenant to connect to, for example 'CALD-DEV'.",
    envvar='SAP_TENANT',
)
@click.option(
    '-u',
    '--username',
    prompt=True,
    help='Username for authentication.',
    envvar='SAP_USERNAME',
)
@click.option(
    '-p',
    '--password',
    prompt=True,
    hide_input=True,
    help='Password for authentication.',
    envvar='SAP_PASSWORD',
)
@click.option(
    '--no-ssl',
    is_flag=True,
    help='Disable SSL validation.',
)
@click.option(
    '-l',
    '--logfile',
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        resolve_path=False,
        path_type=Path,
    ),
    help='Enable logging to a file.',
)
@click.option(
    '-v',
    is_flag=True,
    help='Verbose logging.',
)
@click.option(
    '-debug',
    is_flag=True,
    help='Enable DEBUG logging.',
)
def cli(  # pylint: disable=too-many-arguments
    ctx: click.Context,
    *,
    tenant: str,
    username: str,
    password: str,
    no_ssl: bool = False,
    logfile: Path | None = None,
    v: bool = False,
    debug: bool = False,
) -> None:
    """Command-line interface for Python SAP Incentive Management.

    \b
    You may provide parameters by setting environment variables
    prefixed with 'SAP_' or by passing them as options.
    For example: `export SAP_TENANT=CALD-DEV` is equivalent
    to passing `--tenant CALD-DEV`

    """  # noqa: D301
    ctx.ensure_object(dict)
    ctx.obj['TENANT'] = tenant
    ctx.obj['USERNAME'] = username
    ctx.obj['PASSWORD'] = password
    ctx.obj['SSL'] = not no_ssl

    setup_logging(filename=logfile, verbose=v, debug=debug)
    LOGGER.info("Tenant: '%s', Username: '%s', Ssl: '%s'", tenant, username, not no_ssl)


@cli.command()
@click.pass_context
@click.argument(
    'path',
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
    *,
    path: Path,
) -> None:
    """Deploy rule elements from a directory to the tenant.

    \b
    XML files will be imported using a pipeline job.
    TXT files require a specific name convention:
      - Event Type.txt
      - Credit Type.txt
      - Earning Group.txt
      - Earning Code.txt
      - Fixed Value Type.txt
      - Reason Code.txt

    \b
    Additionally you can control the order of processing by
    prefixing the filenames numerically. For example:
      - 01 Event Type.txt
      - 02 Credit Type.txt
      - 03 Plan.XML

    """  # noqa: D301
    LOGGER.info("Deploy '%s'", path)

    asyncio.run(async_deploy(path, ctx))


@cli.command()
@click.pass_context
def calendars(
    ctx: click.Context,
) -> None:
    """List all calendars."""
    LOGGER.info('List Calendars')

    calendar_names = asyncio.run(async_list_calendars(ctx))
    LOGGER.info('%s', calendar_names)

    for item in calendar_names:
        click.echo(item)


@cli.command()
@click.pass_context
@click.option(
    '--calendar',
    prompt=True,
    type=DynamicChoice(
        'Calendar',
        list_calendars,
    ),
    help="Name of the Calendar. Invoke command 'calendars' for a list of choices.",
    envvar='SAP_CALENDAR',
)
@click.option(
    '--period',
    prompt=False,
    type=click.STRING,
    help="Name of the Period to search. Allows wildcard like '*2024*'.",
)
def periods(
    ctx: click.Context,
    *,
    calendar: str,
    period: str | None = None,
) -> None:
    """List all periods for a calendar."""
    LOGGER.info("List Periods for '%s'", calendar)

    period_names = asyncio.run(async_list_periods(ctx, calendar, period))
    LOGGER.info('%s', period_names)

    for item in period_names:
        click.echo(item)


@cli.command()
@click.pass_context
@click.argument(
    'resource',
    type=click.Choice(
        [
            'CREDITS',
            'MEASUREMENTS',
            'INCENTIVES',
            'COMMISSIONS',
            'DEPOSITS',
            'PAYMENTS',
        ],
        case_sensitive=False,
    ),
)
@click.argument(
    'path',
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        writable=True,
        resolve_path=False,
        path_type=Path,
    ),
)
@click.option(
    '--calendar',
    type=DynamicChoice('Calendar', list_calendars),
    help='Apply Credits filter on Calendar.',
    envvar='SAP_CALENDAR',
)
@click.option(
    '--period',
    type=click.STRING,
    help='Apply Credits filter on Period, use with --calendar.',
    callback=validate_period,
    envvar='SAP_PERIOD',
)
@click.option(
    '--filters',
    multiple=True,
    type=click.STRING,
    help='Optional. Apply a filter, can be provided more then once.',
)
def export(  # pylint: disable=too-many-arguments
    ctx: click.Context,
    *,
    resource: str,
    path: Path,
    calendar: str | None = None,
    period: str | None = None,
    filters: list[str] | None = None,
) -> None:
    """Export Resource to a file."""
    LOGGER.info("Export %s to '%s'", resource, path)
    LOGGER.info(
        "Calendar: '%s', Period: '%s', Filter: '%s'",
        calendar,
        period,
        filters,
    )
    all_filters: list[str] = []
    if calendar and period:
        all_filters.append(str(helpers.Equals('period/calendar/name', calendar)))
        all_filters.append(str(helpers.Equals('period/name', period)))
    if filters:
        all_filters.extend(filters)
    final_filters: str | None = ' and '.join(all_filters) if all_filters else None
    asyncio.run(async_load_resource(ctx, resource, path, final_filters))
    click.echo(path)


if __name__ == '__main__':
    # pylint: disable=missing-kwoa, no-value-for-parameter
    sys.exit(cli(obj={}, auto_envvar_prefix='SAP'))
