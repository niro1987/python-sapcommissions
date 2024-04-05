"""Python SAP Commissions Client."""
import asyncio
import logging
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Any, Final, TypeVar

from aiohttp import ClientError, ClientSession
from pydantic import ValidationError

from sapcommissions import const, exceptions, model
from sapcommissions.helpers import BooleanOperator, LogicalOperator

LOGGER: Final[logging.Logger] = logging.getLogger(__name__)
T = TypeVar("T", bound="model._Resource")


@dataclass
class CommissionsClient:
    """Client interface for interacting with SAP Commissions."""
    tenant: str
    session: ClientSession
    verify_ssl: bool = True
    request_timeout: int = const.REQUEST_TIMEOUT

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
        LOGGER.debug(f"Request: {method=}, {uri=}, {params=}")

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
            not response.status in const.REQUIRED_STATUS[method]
            and response.status != const.STATUS_BAD_REQUEST
        ):
            text = await response.text()
            msg = f"Unexpected status. {response.status}: {text}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        if (
            content_type := response.headers.get("Content-Type")
        ) != "application/json":
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
        LOGGER.debug(f"Create {cls.__name__}({resource})")

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
            if not attr_resource in err.data:
                msg = f"Unexpected payload. {err.data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_data: list[dict[str, Any]] = err.data[attr_resource]
            for errors in error_data:
                if (error_message := errors.get(const.ATTR_ERROR)):
                    if const.ERROR_ALREADY_EXISTS in error_message:
                        raise exceptions.SAPAlreadyExists(error_message) from err
                if any(const.ERROR_MISSING_FIELD in value for value in errors.values()):
                    LOGGER.error(errors)
                    raise exceptions.SAPMissingField(errors) from err
            msg = f"Unexpected error. {error_data}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg) from err

        if not attr_resource in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        json: list[dict[str, Any]] = response[attr_resource]
        data: dict[str, Any] = json[0]
        try:
            return cls(**data)
        except ValidationError as exc:
            for error in exc.errors():
                LOGGER.error(f"{error} on {data}")
            raise

    async def update(self, resource: T) -> T:
        """Update an existing resource."""
        cls = type(resource)
        LOGGER.debug(f"Update {cls.__name__}({resource})")

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
            if not attr_resource in err.data:
                msg = f"Unexpected payload. {err.data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_data: list[dict[str, Any]] = err.data[attr_resource]
            for errors in error_data:
                if (error_message := errors.get(const.ATTR_ERROR)):
                    LOGGER.error(error_message)
                    raise exceptions.SAPResponseError(error_message) from err
            msg = f"Unexpected error. {error_data}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg) from err

        if not attr_resource in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        json: list[dict[str, Any]] = response[attr_resource]
        data: dict[str, Any] = json[0]
        try:
            return cls(**data)
        except ValidationError as exc:
            for error in exc.errors():
                LOGGER.error(f"{error} on {data}")
            raise

    async def delete(self, resource: T) -> bool:
        """Delete a resource."""
        cls = type(resource)
        LOGGER.debug(f"Delete {cls.__name__}({resource})")

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
            if not attr_resource in err.data:
                msg = f"Unexpected payload. {err.data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_data: dict[str, str] = err.data[attr_resource]
            if not seq in error_data:
                msg = f"Unexpected payload. {error_data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_message: str = error_data[seq]
            LOGGER.error(error_message)
            raise exceptions.SAPResponseError(error_message) from err

        if not attr_resource in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        json: dict[str, Any] = response[attr_resource]
        if not seq in json:
            msg = f"Unexpected payload. {json}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        return True

    async def read(
        self,
        resource_cls: type[T],
        *,
        filter: BooleanOperator | LogicalOperator | str | None = None,
        order_by: list[str] | None = None,
    ) -> T:
        """Read the first matching resource."""
        LOGGER.debug(f"Read {resource_cls.__name__} {filter=}")
        list_resources = self.list(
            resource_cls,
            filter=filter,
            order_by=order_by,
            page_size=1,
        )
        return await anext(list_resources)

    async def read_seq(self, resource_cls: type[T], seq: str) -> T:
        """Read the specified resource."""
        LOGGER.debug(f"Read {resource_cls.__name__}({seq})")

        endpoint: str = resource_cls.get_endpoint()
        uri: str = f"{endpoint}({seq})"

        response: dict[str, Any] = await self._request("GET", uri=uri)
        try:
            return resource_cls(**response)
        except ValidationError as exc:
            for error in exc.errors():
                LOGGER.error(f"{error} on {response}")
            raise

    async def reload(self, resource: T) -> T:
        """Reload a fully initiated resource."""
        LOGGER.debug(f"Reload {type(resource).__name__}({resource.seq})")
        return await self.read_seq(type(resource), resource.seq)

    async def list(
        self,
        resource_cls: type[T],
        *,
        filter: BooleanOperator | LogicalOperator | str | None = None,
        order_by: list[str] | None = None,
        page_size: int = 10,
        raw: bool = False,
    ) -> AsyncGenerator[T | dict[str, Any], None]:
        """Lists resources of a specified type with optional filtering and sorting."""
        LOGGER.debug(f"List {resource_cls.__name__} {filter=} {order_by=} {page_size=}")
        if page_size < 1 or page_size > 100:
            raise ValueError(f"page_size ({page_size}) must be between 1 and 100")

        endpoint: str = resource_cls.get_endpoint()
        attr_resource: str = endpoint.split("/")[-1]
        params: dict[str, str] | None = {const.ATTR_TOP: page_size}
        if filter:
            params[const.ATTR_FILTER] = str(filter)
        if order_by:
            params[const.ATTR_ORDERBY] = ",".join(order_by)

        uri: str = endpoint
        attempt: int = 0
        while uri:
            try:
                response = await self._request("GET", uri=uri, params=params)
            except exceptions.SAPConnectionError:
                attempt += 1
                if attempt > 3:
                    raise
                await asyncio.sleep(2.0)
                continue
            else:
                attempt = 0

            if (next := response.get(const.ATTR_NEXT)):
                params = None
                uri = "?".join([endpoint, next.split("?", 1)[-1]])
            else:
                uri = None

            if not attr_resource in response:
                msg = f"Unexpected payload. {response}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg)

            json: list[dict[str, Any]] = response[attr_resource]
            for item in json:
                try:
                    yield item if raw else resource_cls(**item)
                except ValidationError as exc:
                    for error in exc.errors():
                        LOGGER.error(f"{error} on {item}")
                    raise

    async def run_pipeline(self, job: model._Pipeline) -> model.Pipeline:
        """Run a pipeline and retrieves the created Pipeline."""
        LOGGER.debug(f"Run pipeline {type(job).__name__}")
        endpoint: str = job.get_endpoint()
        json: dict[str, Any] = job.model_dump(exclude_none=True)
        LOGGER.debug(f"model_dump: {json}")

        try:
            response: dict[str, Any] = await self._request(
                method="POST",
                uri=endpoint,
                json=[json],
            )
        except exceptions.SAPBadRequest as err:
            if not "pipelines" in err.data:
                msg = f"Unexpected payload. {err.data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            error_data: dict[str, str] = err.data["pipelines"]
            if not "0" in error_data:
                msg = f"Unexpected payload. {error_data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg) from err

            msg = error_data["0"]
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg) from err

        if not "pipelines" in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        json: dict[str, list[str]] = response["pipelines"]
        if not "0" in json:
            msg = f"Unexpected payload. {json}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        seq: str = json["0"][0]
        return await self.read_seq(model.Pipeline, seq)

    async def cancel_pipeline(self, job: model.Pipeline) -> bool:
        """Cancel a running pipeline."""
        cls = type(job)
        LOGGER.debug(f"Cancel {job.command}({job.pipelineRunSeq})")

        endpoint: str = job.get_endpoint()
        uri: str = f"{endpoint}({job.pipelineRunSeq})"

        try:
            response: dict[str, Any] = await self._request(
                method="DELETE",
                uri=uri,
            )
        except exceptions.SAPBadRequest as err:
            if not job.pipelineRunSeq in err.data:
                msg = f"Unexpected payload. {err.data}"
                LOGGER.error(msg)
                raise exceptions.SAPResponseError(msg)

            error_message: str = err.data[job.pipelineRunSeq]
            if const.ERROR_DELETE_PIPELINE in error_message:
                LOGGER.debug(error_message)
                return True
            msg = f"Unexpected payload. {error_message}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg) from err

        if not job.pipelineRunSeq in response:
            msg = f"Unexpected payload. {response}"
            LOGGER.error(msg)
            raise exceptions.SAPResponseError(msg)

        return True
