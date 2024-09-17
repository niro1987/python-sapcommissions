"""Python SAP Commissions Client."""

import asyncio
import logging
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Any, TypeVar

from aiohttp import ClientError, ClientSession
from pydantic_core import ValidationError

from sapcommissions import exceptions, model
from sapcommissions.helpers import BooleanOperator, LogicalOperator, get_alias, retry

LOGGER: logging.Logger = logging.getLogger(__name__)
T = TypeVar("T", bound="model.base.Resource")

REQUEST_TIMEOUT: int = 30
STATUS_NOT_MODIFIED: int = 304
STATUS_BAD_REQUEST: int = 400
STATUS_SERVER_ERROR: int = 500
REQUIRED_STATUS: dict[str, tuple[int, ...]] = {
    "GET": (200,),
    "POST": (200, 201, STATUS_NOT_MODIFIED),
    "PUT": (200, STATUS_NOT_MODIFIED),
    "DELETE": (200,),
}
ATTR_ERROR: str = "_ERROR_"
ATTR_EXPAND: str = "expand"
ATTR_FILTER: str = "$filter"
ATTR_ORDERBY: str = "orderBy"
ATTR_INLINECOUNT: str = "inlineCount"
ATTR_NEXT: str = "next"
ATTR_SKIP: str = "skip"
ATTR_TOP: str = "top"
ATTR_TOTAL: str = "total"
ERROR_ALREADY_EXISTS: str = "TCMP_35004"
ERROR_DELETE_PIPELINE: str = "TCMP_60255"
ERROR_MISSING_FIELD: str = "TCMP_1002"
ERROR_NOT_FOUND: str = "TCMP_09007"
ERROR_REFERRED_BY: str = "TCMP_35001"
ERROR_REMOVE_FAILED: str = "TCMP_35243"
MIN_PAGE_SIZE: int = 1
MAX_PAGE_SIZE: int = 100


@dataclass
class CommissionsClient:
    """Client interface for interacting with SAP Commissions."""

    tenant: str
    session: ClientSession
    verify_ssl: bool = True
    request_timeout: int = REQUEST_TIMEOUT

    @property
    def host(self) -> str:
        """The fully qualified hostname."""
        return f"https://{self.tenant}.callidusondemand.com"

    async def _request(
        self,
        method: str,
        uri: str,
        params: dict | None = None,
        json: list | None = None,
    ) -> dict[str, Any]:
        """Send a request."""
        LOGGER.debug("Request: %s, %s, %s", method, uri, params)

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(
                    method=method,
                    url=f"{self.host}/{uri}",
                    params=params,
                    json=json,
                    ssl=self.verify_ssl,
                )
        except TimeoutError as err:
            msg = "Timeout while connecting"
            LOGGER.error(msg)
            raise exceptions.SAPConnectionError(msg) from err
        except ClientError as err:
            msg = "Could not connect"
            LOGGER.error(msg)
            raise exceptions.SAPConnectionError(msg) from err

        if method in ("POST", "PUT") and response.status == STATUS_NOT_MODIFIED:
            msg = "Resource not modified"
            raise exceptions.SAPNotModified(msg)

        if (
            response.status not in REQUIRED_STATUS[method]
            and response.status != STATUS_BAD_REQUEST
        ):
            text = await response.text()
            msg = f"Unexpected status. {response.status}: {text}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        if (content_type := response.headers.get("Content-Type")) != "application/json":
            text = await response.text()
            msg = f"Unexpected Content-Type. {content_type}: {text}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        json_data = await response.json()
        if response.status in (STATUS_BAD_REQUEST, STATUS_SERVER_ERROR):
            raise exceptions.SAPBadRequest(json_data)
        return json_data

    async def create(self, resource: T) -> T:
        """Create a new resource."""
        cls = type(resource)
        LOGGER.debug("Create %s(%s)", cls.__name__, resource)

        attr_resource: str = resource.attr_endpoint.split("/")[-1]
        json: dict[str, Any] = resource.model_dump(by_alias=True, exclude_none=True)

        try:
            response: dict[str, Any] = await self._request(
                method="POST",
                uri=resource.attr_endpoint,
                json=[json],
            )
        except exceptions.SAPBadRequest as err:
            if attr_resource not in err.data:
                msg = f"Unexpected payload. {err.data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_data: list[dict[str, Any]] = err.data[attr_resource]
            for errors in error_data:
                if error_message := errors.get(ATTR_ERROR):
                    if ERROR_ALREADY_EXISTS in error_message:
                        raise exceptions.SAPAlreadyExists(error_message) from err
                if any(ERROR_MISSING_FIELD in value for value in errors.values()):
                    LOGGER.error(errors)
                    raise exceptions.SAPMissingField(errors) from err
            msg = f"Unexpected error. {error_data}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg) from err

        if attr_resource not in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        json_data: list[dict[str, Any]] = response[attr_resource]
        data: dict[str, Any] = json_data[0]
        try:
            return cls(**data)
        except ValidationError as exc:
            for error in exc.errors():
                LOGGER.error("%s on %s", error, data)
            raise

    async def update(self, resource: T) -> T:
        """Update an existing resource."""
        cls = type(resource)
        LOGGER.debug("Update %s(%s)", cls.__name__, resource)

        attr_resource: str = resource.attr_endpoint.split("/")[-1]
        json: dict[str, Any] = resource.model_dump(by_alias=True, exclude_none=True)

        try:
            response: dict[str, Any] = await self._request(
                method="PUT",
                uri=resource.attr_endpoint,
                json=[json],
            )
        except exceptions.SAPNotModified:
            return resource
        except exceptions.SAPBadRequest as err:
            if attr_resource not in err.data:
                msg = f"Unexpected payload. {err.data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_data: list[dict[str, Any]] = err.data[attr_resource]
            for errors in error_data:
                if error_message := errors.get(ATTR_ERROR):
                    LOGGER.error(error_message)
                    raise exceptions.SAPResponseError(error_message) from err
            msg = f"Unexpected error. {error_data}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg) from err

        if attr_resource not in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        json_data: list[dict[str, Any]] = response[attr_resource]
        data: dict[str, Any] = json_data[0]
        try:
            return cls(**data)
        except ValidationError as exc:
            for error in exc.errors():
                LOGGER.error("%s on %s", error, data)
            raise

    async def delete(self, resource: T) -> bool:
        """Delete a resource."""
        cls = type(resource)
        LOGGER.debug("Delete %s(%s)", cls.__name__, resource)

        attr_resource: str = resource.attr_endpoint.split("/")[-1]
        if not (seq := resource.seq):
            raise ValueError(f"Resource {cls.__name__} has no unique identifier")
        uri: str = f"{resource.attr_endpoint}({seq})"

        try:
            response: dict[str, Any] = await self._request(
                method="DELETE",
                uri=uri,
            )
        except exceptions.SAPBadRequest as err:
            if attr_resource not in err.data:
                msg = f"Unexpected payload. {err.data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_data: dict[str, str] = err.data[attr_resource]
            if seq not in error_data:
                msg = f"Unexpected payload. {error_data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_message: str = error_data[seq]
            LOGGER.error(error_message)
            raise exceptions.SAPResponseError(error_message) from err

        if attr_resource not in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        json: dict[str, Any] = response[attr_resource]
        if seq not in json:
            msg = f"Unexpected payload. {json}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        return True

    async def read_all(  # pylint: disable=too-many-arguments,too-many-locals  # noqa: PLR0913
        self,
        resource_cls: type[T],
        *,
        filters: BooleanOperator | LogicalOperator | str | None = None,
        order_by: list[str] | None = None,
        page_size: int = 10,
    ) -> AsyncGenerator[T, None]:
        """Read all matching resources."""
        LOGGER.debug(
            "List %s filters=%s order_by=%s page_size=%s",
            resource_cls.__name__,
            str(filters),
            ",".join(order_by) if order_by else "None",
            page_size,
        )
        if page_size < MIN_PAGE_SIZE or page_size > MAX_PAGE_SIZE:
            raise ValueError(
                f"page_size ({page_size}) must be between {MIN_PAGE_SIZE} and {MAX_PAGE_SIZE}"
            )

        attr_resource: str = resource_cls.attr_endpoint.split("/")[-1]
        params: dict[str, str | int] = {ATTR_TOP: page_size}
        if filters:
            params[ATTR_FILTER] = str(filters)
        if order_by:
            params[ATTR_ORDERBY] = ",".join(order_by)
        if expand_alias := [
            get_alias(resource_cls, field_name) for field_name in resource_cls.expands()
        ]:
            params[ATTR_EXPAND] = ",".join(expand_alias)

        uri: str | None = resource_cls.attr_endpoint
        while True:
            response = await retry(
                self._request,
                "GET",
                uri=uri,
                params=params,
                exceptions=exceptions.SAPConnectionError,
            )

            if attr_resource not in response:
                msg = f"Unexpected payload. {response}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg)

            json: list[dict[str, Any]] = response[attr_resource]
            for item in json:
                try:
                    yield resource_cls(**item)
                except ValidationError as exc:
                    for error in exc.errors():
                        LOGGER.error("%s on %s", error, item)
                    raise

            if not (next_uri := response.get(ATTR_NEXT)):
                break

            params = {}
            uri = "api" + next_uri

    async def read_first(
        self,
        resource_cls: type[T],
        *,
        filters: BooleanOperator | LogicalOperator | str | None = None,
        order_by: list[str] | None = None,
    ) -> T | None:
        """Read the first matching resource.

        TODO: Fix type error
        """
        LOGGER.debug("Read %s %s", resource_cls.__name__, f"filters={filters}")
        list_resources = self.read_all(
            resource_cls,
            filters=filters,
            order_by=order_by,
            page_size=1,
        )
        try:
            return await anext(list_resources)  # type: ignore[arg-type]
        except StopAsyncIteration:
            return None

    async def read_seq(self, resource_cls: type[T], seq: str) -> T:
        """Read the specified resource."""
        LOGGER.debug("Read Seq %s(%s)", resource_cls.__name__, seq)

        uri: str = f"{resource_cls.attr_endpoint}({seq})"
        params: dict[str, str] = {}
        if expand_alias := [
            get_alias(resource_cls, field_name) for field_name in resource_cls.expands()
        ]:
            params[ATTR_EXPAND] = ",".join(expand_alias)

        response: dict[str, Any] = await self._request("GET", uri=uri, params=params)
        try:
            return resource_cls(**response)
        except ValidationError as exc:
            for error in exc.errors():
                LOGGER.error("%s on %s", error, response)
            raise

    async def read(self, resource: T) -> T:
        """Reload a fully initiated resource."""
        cls = type(resource)
        LOGGER.debug("Read %s(%s)", cls.__name__, resource.seq)
        if not (seq := resource.seq):
            raise ValueError(f"Resource {cls.__name__} has no unique identifier")
        return await self.read_seq(cls, seq)

    async def run_pipeline(self, job: model.pipeline._PipelineJob) -> model.Pipeline:
        """Run a pipeline and retrieves the created Pipeline."""
        LOGGER.debug("Run pipeline %s", type(job).__name__)
        json: dict[str, Any] = job.model_dump(by_alias=True, exclude_none=True)

        try:
            response: dict[str, Any] = await self._request(
                method="POST",
                uri=job.attr_endpoint,
                json=[json],
            )
        except exceptions.SAPBadRequest as err:
            if "pipelines" not in err.data:
                msg = f"Unexpected payload. {err.data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_data: dict[str, str] = err.data["pipelines"]
            if "0" not in error_data:
                msg = f"Unexpected payload. {error_data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            msg = error_data["0"]
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg) from err

        if "pipelines" not in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        json_data: dict[str, list[str]] = response["pipelines"]
        if "0" not in json_data:
            msg = f"Unexpected payload. {json_data}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        seq: str = json_data["0"][0]
        return await self.read_seq(model.Pipeline, seq)

    async def cancel_pipeline(self, job: model.Pipeline) -> bool:
        """Cancel a running pipeline."""
        LOGGER.debug("Cancel %s(%s)", job.command, job.pipeline_run_seq)

        uri: str = f"{job.attr_endpoint}({job.pipeline_run_seq})"
        try:
            response: dict[str, Any] = await self._request(
                method="DELETE",
                uri=uri,
            )
        except exceptions.SAPBadRequest as err:
            if job.pipeline_run_seq not in err.data:
                msg = f"Unexpected payload. {err.data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_message: str = err.data[job.pipeline_run_seq]
            if ERROR_DELETE_PIPELINE in error_message:
                # TCMP_60255:E: An error occurred while attempting to delete a job.
                # The Grid Server returned with the message:
                # [GSVRH] Setting Job runStatus to Cancel, but the Controller returned
                # the following error: ++-error::[Controller] unknown command: delJob
                return True
            msg = f"Unexpected payload. {error_message}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg) from err

        if job.pipeline_run_seq not in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        return True
