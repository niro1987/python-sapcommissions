"""Deploy module for Python SAP Commissions Client."""
import asyncio
import csv
import logging
import re
from pathlib import Path
from typing import Any, Callable, Final

from aiohttp import BasicAuth, ClientSession
from dotenv import dotenv_values

from sapcommissions import CommissionsClient, model
from sapcommissions.const import PipelineState, PipelineStatus
from sapcommissions.exceptions import SAPAlreadyExists, SAPConnectionError

LOGGER: Final[logging.Logger] = logging.getLogger(__name__)

RE_CREDIT_TYPE: Final[re.Pattern] = re.compile(rf"^([a-z0-9_.-]+)?(Credit Type)\.txt$", re.IGNORECASE)
RE_EARNING_CODE: Final[re.Pattern] = re.compile(r"^([a-z0-9_.-]+)?(Earning Code)\.txt$", re.IGNORECASE)
RE_EARNING_GROUP: Final[re.Pattern] = re.compile(r"^([a-z0-9_.-]+)?(Earning Group)\.txt$", re.IGNORECASE)
RE_EVENT_TYPE: Final[re.Pattern] = re.compile(r"^([a-z0-9_.-]+)?(Event Type)\.txt$", re.IGNORECASE)
RE_FIXED_VALUE_TYPE: Final[re.Pattern] = re.compile(r"^([a-z0-9_.-]+)?(Fixed Value Type)\.txt$", re.IGNORECASE)
RE_REASON_CODE: Final[re.Pattern] = re.compile(r"^([a-z0-9_.-]+)?(Reason Code)\.txt$", re.IGNORECASE)
RE_XML: Final[re.Pattern] = re.compile(r"^([a-z0-9_.-]+)?([a-z0-9_.-]+)\.xml$", re.IGNORECASE)

def _file_cls(file: Path) -> model._Resource:
    if re.match(RE_CREDIT_TYPE, file.name):
        return model.CreditType
    if re.match(RE_EARNING_CODE, file.name):
        return model.EarningCode
    if re.match(RE_EARNING_GROUP, file.name):
        return model.EarningGroup
    if re.match(RE_EVENT_TYPE, file.name):
        return model.EventType
    if re.match(RE_FIXED_VALUE_TYPE, file.name):
        return model.FixedValueType
    if re.match(RE_REASON_CODE, file.name):
        return model.ReasonCode
    if re.match(RE_XML, file.name):
        return model.XMLImport
    raise ValueError(f"Unidentified filetype", {"filename": file.name})

async def _retry(
    coroutine_function: Callable,
    *args,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] | None = None,
    retries: int = 3,
    delay: float = 3.0,
    **kwargs
) -> Any:
    """
    Retry a coroutine function a specified number of times, with an optional
    specific exception(s) to catch.

    Returns:
        The result of the coroutine function if successful.

    Raises:
        The last exception caught if retries are exhausted.
    """
    if exceptions is not None and not isinstance(exceptions, tuple):
        exceptions = (exceptions,)

    for attempt in range(retries):
        try:
            return await coroutine_function(*args, **kwargs)
        except Exception as err:
            if not isinstance(err, exceptions):
                raise
            LOGGER.debug(f"Failed attempt {attempt + 1}: {err}")
            if attempt + 1 >= retries:
                raise
            await asyncio.sleep(delay)


async def deploy_from_path(
    client: CommissionsClient,
    path: Path,
) -> dict[Path, list[model._Resource]]:
    """Deploy."""
    LOGGER.debug(f"Deploy {path}")
    # This is to make sure we recognize each file before we attempt to deploy.
    files_with_cls: list[tuple[Path, model._Resource]] = [
        (file, _file_cls(file))
        for file in sorted(path.iterdir(), key=lambda x: x.name)
        if file.is_file()
    ]
    results: dict[Path, list[model._Resource]] = {}
    for (file, resource_cls) in files_with_cls:
        if resource_cls is model.XMLImport:
            results[file] = await deploy_xml(client, file)
        else:
            results[file] = await deploy_resources_from_file(client, file, resource_cls)
    return results

async def deploy_resources_from_file(
    client: CommissionsClient,
    file: Path,
    resource_cls: model._Resource,
) -> list[model._Resource]:
    """Deploy file."""
    LOGGER.info(f"Deploy file: {file}")
    with open(file, mode="r", encoding="utf-8", newline="") as f_in:
        reader = csv.DictReader(f_in)
        resources: list[model._Resource] = [
            resource_cls(**row) for row in reader
        ]
    tasks = [deploy_resource(client, resource) for resource in resources]
    return await asyncio.gather(*tasks)

async def deploy_resource(
    client: CommissionsClient,
    resource: model._Resource
) -> model._Resource:
    """Deploy resource."""
    resource_cls: model._Resource = resource.__class__
    LOGGER.debug(f"Deploy {resource_cls.__name__}: {resource}")

    result: model._Resource | None = None
    try:
        result = await _retry(
            client.create,
            resource,
            exceptions=SAPConnectionError,
        )
        LOGGER.info(f"{resource_cls.__name__} created: {result}")
    except SAPAlreadyExists:  # Resource exists, update instead
        result = await _retry(
            client.update,
            resource,
            exceptions=SAPConnectionError,
        )
        LOGGER.info(f"{resource_cls.__name__} updated: {result}")
    return result

async def deploy_xml(
    client: CommissionsClient,
    file: Path,
) -> list[model.Pipeline]:
    """Deploy XML Plan data."""
    LOGGER.debug(f"Deploy Plan data: {file}")

    job: model.XMLImport = model.XMLImport(
        xmlFileName=file.name,
        xmlFileContent=file.read_text("UTF-8"),
        updateExistingObjects=True,
    )
    result: model.Pipeline = await _retry(
        client.run_pipeline,
        job,
        exceptions=SAPConnectionError,
    )
    while result.state != PipelineState.DONE:
        await asyncio.sleep(2)
        result = await _retry(
            client.reload,
            result,
            exceptions=SAPConnectionError,
        )

    if result.status != PipelineStatus.SUCCESSFUL:
        LOGGER.error(f"XML Import failed (errors: {result.numErrors})!")
    else:
        LOGGER.info(f"Plan data imported: {file}")
    return [result]


async def main():
    config = dotenv_values("tests/.env")
    auth = BasicAuth(login=config["SAP_USERNAME"], password=config["SAP_PASSWORD"])
    path = Path("tests/deploy")

    async with ClientSession(auth=auth) as session:
        client = CommissionsClient(
            tenant="VFNL-MDEV",
            session=session,
            verify_ssl=False,
        )
        result = await deploy_from_path(client, path)
        print(result)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(name)-20s | %(levelname)-8s | %(message)s",
    )
    base_logger = logging.getLogger("sapcommissions")
    base_logger.setLevel(logging.ERROR)

    asyncio.run(main())
