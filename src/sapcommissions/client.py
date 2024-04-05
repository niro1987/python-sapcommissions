"""Python SAP Commissions Client."""

import asyncio
import logging
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Any, TypeVar

from aiohttp import ClientError, ClientSession
from pydantic import ValidationError

from sapcommissions import const, exceptions, model
from sapcommissions.helpers import BooleanOperator, LogicalOperator, retry

LOGGER: logging.Logger = logging.getLogger(__name__)
T = TypeVar("T", bound="model._Resource")

REQUEST_TIMEOUT: int = 30
STATUS_NOT_MODIFIED: int = 304
STATUS_BAD_REQUEST: int = 400
STATUS_SERVER_ERROR: int = 500
REQUIRED_STATUS: dict[str, tuple[int]] = {
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

        if method in ("POST", "PUT") and response.status == const.STATUS_NOT_MODIFIED:
            msg = "Resource not modified"
            raise exceptions.SAPNotModified(msg)

        if (
            response.status not in const.REQUIRED_STATUS[method]
            and response.status != const.STATUS_BAD_REQUEST
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

        json = await response.json()
        if response.status in (const.STATUS_BAD_REQUEST, const.STATUS_SERVER_ERROR):
            raise exceptions.SAPBadRequest(json)
        return json

    async def create(self, resource: T) -> T:
        """Create a new resource."""
        cls = type(resource)
        LOGGER.debug("Create %s(%s)", cls.__name__, resource)

        endpoint: str = resource.get_endpoint()
        attr_resource: str = endpoint.split("/")[-1]
        json: dict[str, Any] = resource.model_dump(exclude_none=True)

        try:
            response: dict[str, Any] = await self._request(
                method="POST",
                uri=endpoint,
                json=[json],
            )
        except exceptions.SAPBadRequest as err:
            if attr_resource not in err.data:
                msg = f"Unexpected payload. {err.data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_data: list[dict[str, Any]] = err.data[attr_resource]
            for errors in error_data:
                if error_message := errors.get(const.ATTR_ERROR):
                    if const.ERROR_ALREADY_EXISTS in error_message:
                        raise exceptions.SAPAlreadyExists(error_message) from err
                if any(const.ERROR_MISSING_FIELD in value for value in errors.values()):
                    LOGGER.error(errors)
                    raise exceptions.SAPMissingField(errors) from err
            msg = f"Unexpected error. {error_data}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg) from err

        if attr_resource not in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        json: list[dict[str, Any]] = response[attr_resource]
        data: dict[str, Any] = json[0]
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

        endpoint: str = resource.get_endpoint()
        attr_resource: str = endpoint.split("/")[-1]
        json: dict[str, Any] = resource.model_dump(exclude_none=True)

        try:
            response: dict[str, Any] = await self._request(
                method="PUT",
                uri=endpoint,
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
                if error_message := errors.get(const.ATTR_ERROR):
                    LOGGER.error(error_message)
                    raise exceptions.SAPResponseError(error_message) from err
            msg = f"Unexpected error. {error_data}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg) from err

        if attr_resource not in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        json: list[dict[str, Any]] = response[attr_resource]
        data: dict[str, Any] = json[0]
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

        endpoint: str = resource.get_endpoint()
        attr_resource: str = endpoint.split("/")[-1]
        seq: str = resource.seq
        uri: str = f"{endpoint}({seq})"

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

    async def read(
        self,
        resource_cls: type[T],
        *,
        filters: BooleanOperator | LogicalOperator | str | None = None,
        order_by: list[str] | None = None,
    ) -> T:
        """Read the first matching resource."""
        LOGGER.debug("Read %s %s", resource_cls.__name__, f"filters={filters}")
        list_resources = self.list(
            resource_cls,
            filters=filters,
            order_by=order_by,
            page_size=1,
        )
        return await anext(list_resources)

    async def read_seq(self, resource_cls: type[T], seq: str) -> T:
        """Read the specified resource."""
        LOGGER.debug("Read %s(%s)", resource_cls.__name__, seq)

        endpoint: str = resource_cls.get_endpoint()
        uri: str = f"{endpoint}({seq})"

        response: dict[str, Any] = await self._request("GET", uri=uri)
        try:
            return resource_cls(**response)
        except ValidationError as exc:
            for error in exc.errors():
                LOGGER.error("%s on %s", error, response)
            raise

    async def reload(self, resource: T) -> T:
        """Reload a fully initiated resource."""
        LOGGER.debug("Reload %s(%s)", type(resource).__name__, resource.seq)
        return await self.read_seq(type(resource), resource.seq)

    async def list(
        self,
        resource_cls: type[T],
        *,
        filters: BooleanOperator | LogicalOperator | str | None = None,
        order_by: list[str] | None = None,
        page_size: int = 10,
    ) -> AsyncGenerator[T | dict[str, Any], None]:
        """List resources of a specified type with optional filtering and sorting."""
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

        endpoint: str = resource_cls.get_endpoint()
        attr_resource: str = endpoint.split("/")[-1]
        params: dict[str, str] | None = {const.ATTR_TOP: page_size}
        if filters:
            params[const.ATTR_FILTER] = str(filters)
        if order_by:
            params[const.ATTR_ORDERBY] = ",".join(order_by)

        while endpoint:
            response = await retry(
                self._request,
                "GET",
                uri=endpoint,
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

            if next_uri := response.get(const.ATTR_NEXT):
                params = None
                endpoint = "?".join([endpoint, next_uri.split("?", 1)[-1]])
            else:
                break

    async def run_pipeline(self, job: model._Pipeline) -> model.Pipeline:
        """Run a pipeline and retrieves the created Pipeline."""
        LOGGER.debug("Run pipeline %s", type(job).__name__)
        endpoint: str = job.get_endpoint()
        json: dict[str, Any] = job.model_dump(exclude_none=True)
        LOGGER.debug("model_dump: %s", json)

        try:
            response: dict[str, Any] = await self._request(
                method="POST",
                uri=endpoint,
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

        json: dict[str, list[str]] = response["pipelines"]
        if "0" not in json:
            msg = f"Unexpected payload. {json}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        seq: str = json["0"][0]
        return await self.read_seq(model.Pipeline, seq)

    async def cancel_pipeline(self, job: model.Pipeline) -> bool:
        """Cancel a running pipeline."""
        LOGGER.debug("Cancel %s(%s)", job.command, job.pipelineRunSeq)

        endpoint: str = job.get_endpoint()
        uri: str = f"{endpoint}({job.pipelineRunSeq})"

        try:
            response: dict[str, Any] = await self._request(
                method="DELETE",
                uri=uri,
            )
        except exceptions.SAPBadRequest as err:
            if job.pipelineRunSeq not in err.data:
                msg = f"Unexpected payload. {err.data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_message: str = err.data[job.pipelineRunSeq]
            if const.ERROR_DELETE_PIPELINE in error_message:
                LOGGER.debug(error_message)
                return True
            msg = f"Unexpected payload. {error_message}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg) from err

        if job.pipelineRunSeq not in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        return True
