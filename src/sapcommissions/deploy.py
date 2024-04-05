"""Deploy module for Python SAP Commissions Client."""

import asyncio
import csv
import logging
import re
from pathlib import Path
from typing import Final

from sapcommissions import CommissionsClient, model
from sapcommissions.const import PipelineState, PipelineStatus
from sapcommissions.exceptions import SAPAlreadyExists, SAPConnectionError
from sapcommissions.helpers import retry

LOGGER: logging.Logger = logging.getLogger(__name__)

RE_CREDIT_TYPE: Final[re.Pattern] = re.compile(
    r"^([a-z0-9_.-]+)?(Credit Type)\.txt$", re.IGNORECASE
)
RE_EARNING_CODE: Final[re.Pattern] = re.compile(
    r"^([a-z0-9_.-]+)?(Earning Code)\.txt$", re.IGNORECASE
)
RE_EARNING_GROUP: Final[re.Pattern] = re.compile(
    r"^([a-z0-9_.-]+)?(Earning Group)\.txt$", re.IGNORECASE
)
RE_EVENT_TYPE: Final[re.Pattern] = re.compile(
    r"^([a-z0-9_.-]+)?(Event Type)\.txt$", re.IGNORECASE
)
RE_FIXED_VALUE_TYPE: Final[re.Pattern] = re.compile(
    r"^([a-z0-9_.-]+)?(Fixed Value Type)\.txt$", re.IGNORECASE
)
RE_REASON_CODE: Final[re.Pattern] = re.compile(
    r"^([a-z0-9_.-]+)?(Reason Code)\.txt$", re.IGNORECASE
)
RE_XML: Final[re.Pattern] = re.compile(
    r"^([a-z0-9_.-]+)?([a-z0-9_.-]+)\.xml$", re.IGNORECASE
)


def _file_cls(file: Path) -> model._Resource:
    """Determine the resource class based on the filename."""
    file_mapping: dict[re.Pattern, type[model._Resource]] = {
        RE_CREDIT_TYPE: model.CreditType,
        RE_EARNING_CODE: model.EarningCode,
        RE_EARNING_GROUP: model.EarningGroup,
        RE_EVENT_TYPE: model.EventType,
        RE_FIXED_VALUE_TYPE: model.FixedValueType,
        RE_REASON_CODE: model.ReasonCode,
        RE_XML: model.XMLImport,
    }
    for pattern, resource_cls in file_mapping.items():
        if re.match(pattern, file.name):
            return resource_cls
    raise ValueError("Unidentified filetype", file.name)


async def deploy_from_path(
    client: CommissionsClient,
    path: Path,
) -> dict[Path, list[model._Resource]]:
    """Deploy."""
    LOGGER.debug("Deploy %s", path)
    # This is to make sure we recognize each file before we attempt to deploy.
    files_with_cls: list[tuple[Path, model._Resource]] = [
        (file, _file_cls(file))
        for file in sorted(path.iterdir(), key=lambda x: x.name)
        if file.is_file()
    ]
    results: dict[Path, list[model._Resource]] = {}
    for file, resource_cls in files_with_cls:
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
    LOGGER.info("Deploy file: %s", file)
    with open(file, encoding="utf-8", newline="") as f_in:
        reader = csv.DictReader(f_in)
        resources: list[model._Resource] = [resource_cls(**row) for row in reader]
    tasks = [deploy_resource(client, resource) for resource in resources]
    return await asyncio.gather(*tasks)


async def deploy_resource(
    client: CommissionsClient, resource: model._Resource
) -> model._Resource:
    """Deploy resource."""
    resource_cls: model._Resource = resource.__class__
    LOGGER.debug("Deploy %s: %s", resource_cls.__name__, resource)

    result: model._Resource | None = None
    try:
        result = await retry(
            client.create,
            resource,
            exceptions=SAPConnectionError,
        )
        LOGGER.info("%s created: %s", resource_cls.__name__, result)
    except SAPAlreadyExists:  # Resource exists, update instead
        result = await retry(
            client.update,
            resource,
            exceptions=SAPConnectionError,
        )
        LOGGER.info("%s updated: %s", resource_cls.__name__, result)
    return result


async def deploy_xml(
    client: CommissionsClient,
    file: Path,
) -> list[model.Pipeline]:
    """Deploy XML Plan data."""
    LOGGER.debug("Deploy Plan data: %s", file)

    job: model.XMLImport = model.XMLImport(
        xmlFileName=file.name,
        xmlFileContent=file.read_text("UTF-8"),
        updateExistingObjects=True,
    )
    result: model.Pipeline = await retry(
        client.run_pipeline,
        job,
        exceptions=SAPConnectionError,
    )
    while result.state != PipelineState.Done:
        await asyncio.sleep(2)
        result = await retry(
            client.reload,
            result,
            exceptions=SAPConnectionError,
        )

    if result.status != PipelineStatus.Successful:
        LOGGER.error("XML Import failed (errors: %s)!", result.numErrors)
    else:
        LOGGER.info("Plan data imported: %s", file)
    return [result]
