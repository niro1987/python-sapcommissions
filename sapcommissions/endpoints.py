"""Endpoints are used to interact with SAP Commissions objects."""
import logging
from datetime import date
from typing import Any

from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from requests.models import Response
from requests.sessions import Session
from urllib3 import disable_warnings

from sapcommissions import Connection, resources
from sapcommissions.exceptions import AuthenticationError, ClientError, ServerError

LOGGER = logging.getLogger(__name__)


class _Client(Session):
    """Interacts with SAP Commissions REST API. Extends requests.Session."""

    def __init__(
        self,
        baseUrl: str,
        username: str,
        password: str,
        verifySsl: bool = True,
    ) -> None:
        """Initialize an endpoint to interact with SAP Commissions."""
        super().__init__()
        self.baseUrl: str = baseUrl
        self.auth = HTTPBasicAuth(username, password)
        if verifySsl is False:
            disable_warnings()
            self.verify = verifySsl

    def request(  # pylint: disable=arguments-differ
        self,
        method: str,
        uri: str,
        parameters: dict[str, str] | None = None,
        body: list[dict[str, str]] | None = None,
    ) -> dict[str, Any | list[dict[str, Any]]] | Response:
        """Perform an HTTP request to the SAP Commissions REST API."""
        LOGGER.debug("%s %s %s", method.upper(), uri, parameters)
        url: str = self.baseUrl + uri
        with super().request(
            method=method,
            url=url,
            params=parameters,
            json=body,
        ) as response:
            try:
                response.raise_for_status()
                if "application/json" not in response.headers.get("content-type", ""):
                    raise ValueError("Response content-type is not application/json.")
                return response.json()
            except HTTPError as error:
                LOGGER.error(
                    "%s %s %s %s",
                    method.upper(),
                    response.status_code,
                    uri,
                    response.text,
                )
                if 401 <= response.status_code <= 403:
                    raise AuthenticationError(response.text) from error
                if 400 <= response.status_code < 500:
                    raise ClientError(response.text) from error
                if 500 <= response.status_code < 600:
                    raise ServerError(response.text) from error
        return None

    def get(  # pylint: disable=arguments-renamed,arguments-differ
        self,
        uri: str,
        parameters: dict[str, str] | None = None,
    ) -> dict[str, Any | list[dict[str, Any]]]:
        """Perform a GET request to the SAP Commissions REST API."""
        return self.request("GET", uri, parameters=parameters)

    def delete(  # pylint: disable=arguments-renamed,arguments-differ
        self, uri: str, parameters: dict[str, str] | None = None
    ) -> dict[str, Any | list[dict[str, Any]]]:
        """Perform a DELETE request to the SAP Commissions REST API."""
        return self.request("DELETE", uri, parameters=parameters)

    def post(  # pylint: disable=arguments-renamed,arguments-differ
        self, uri: str, body: list[dict[str, str]]
    ) -> dict[str, Any | list[dict[str, Any]]]:
        """Perform a POST request to the SAP Commissions REST API."""
        return self.request("POST", uri, body=body)

    def put(  # pylint: disable=arguments-renamed,arguments-differ
        self, uri: str, body: list[dict[str, str]]
    ) -> dict[str, Any | list[dict[str, Any]]]:
        """Perform a PUT request to the SAP Commissions REST API."""
        return self.request("PUT", uri, body=body)


class _Endpoint:
    """Provides a base template for an endpoint method."""

    resource: resources._Resource

    def __init__(self, connection: Connection) -> None:
        """Initialize a base template for an endpoint method."""
        self._client = _Client(
            baseUrl=connection.apiUrl,
            username=connection.username,
            password=connection.password,
            verifySsl=connection.verifySsl,
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    @property
    def name(self) -> str:
        """Returns the name of the resource."""
        return self.resource._name  # pylint: disable=protected-access

    @property
    def url(self) -> str:
        """Returns the API URL of the endpoint."""
        return f"/v2/{self.name}"


class _Create(_Endpoint):
    def create(self, instance: resources._Resource) -> resources._Resource:
        """
        Create a new resource for the endpoint.

        Parameters
        ----------
        instances : resources._Resource
            Resource to create.
        """
        LOGGER.info("Create %s", self.name)

        assert isinstance(instance, self.resource)
        json_data = instance.to_dict()

        response = self._client.post(self.url, [json_data])
        data = response[self.name]
        created = self.resource.from_dict(data[0])

        return created


class _CreateVersions(_Endpoint):
    def create_versions(
        self, seq: int, versions: list[resources._Resource]
    ) -> list[resources._Resource]:
        """
        Create versions of an existing resource.

        Parameters
        ----------
        seq : int
            Resource system identifier.
        versions : list[resources._Resource]
            List of resource versions to create.
        """
        LOGGER.info("Create versions for %s with seq %s", self.name, seq)

        assert isinstance(seq, int)
        assert isinstance(versions, list)
        for version in versions:
            assert isinstance(version, self.resource)
        json_data = [version.to_dict() for version in versions]

        response = self._client.post(self.url + f"({seq})/versions", json_data)
        if response is not None:
            data = response[self.name]
            created_versions = [self.resource.from_dict(item) for item in data]
        else:
            created_versions = versions

        return created_versions


class _Delete(_Endpoint):
    def delete(self, seq: int) -> str:
        """
        Delete an existing resource.

        Parameters
        ----------
        seq : int
            Resource system identifier to delete.
        """
        LOGGER.info("Delete %s with seq %s", self.name, seq)

        assert isinstance(seq, int)

        response = self._client.delete(f"{self.url}({seq})")
        data = response[self.name]
        message = data[str(seq)]

        return message


class _DeleteVersions(_Endpoint):
    def delete_versions(
        self,
        seq: int,
        effectiveStartDate: date,
        effectiveEndDate: date,
        fillFromRight: bool = False,
    ) -> str:
        """
        Deletes the given version for an existing resource.

        Parameters
        ----------
        seq : int
            Resource system identifier.
        effectiveStartDate : date
            Resource effectiveStartDate.
        effectiveEndDate : date
            Resource effectiveEndDate.
        fillFromRight : bool
            If true, then the gap will be filled by the right (next) version,
            otherwise by the left (prev) version. Default is false (prev).
        """
        LOGGER.info("Delete versions for %s with seq %s", self.name, seq)

        query = {}
        assert isinstance(seq, int)
        assert isinstance(effectiveStartDate, date)
        query["effectiveStartDate"] = effectiveStartDate.strftime("%Y-%m-%d")
        assert isinstance(effectiveEndDate, date)
        query["effectiveEndDate"] = effectiveEndDate.strftime("%Y-%m-%d")
        assert isinstance(fillFromRight, bool)
        query["fillFromRight"] = fillFromRight

        response = self._client.delete(self.url + f"({seq})/versions", query)
        data = response[self.name]
        message = data[0]

        return message


class _Get(_Endpoint):
    def get(self, seq: int) -> resources._Resource:
        """
        Reads all of the attributes of an existing resource.

        Parameters
        ----------
        seq : int
            Resource system identifier.
        """
        LOGGER.info("Get %s with seq %s", self.name, seq)

        assert isinstance(seq, int)

        response = self._client.get(self.url + f"({seq})")
        item = self.resource.from_dict(response)

        return item


class _GetVersions(_Endpoint):
    def get_versions(
        self,
        seq: int,
        startDate: date = None,
        endDate: date = None,
    ) -> list[resources._Resource]:
        """
        Returns all of the versions of a resource.

        Parameters
        ----------
        seq : int
            Resource system identifier.
        startDate : date
            Filter List for resources effective for startDate.
        endDate : date
            Filter List for resources effective for endDate.
        """
        LOGGER.info("Get versions of %s with seq %s", self.name, seq)

        query = {}
        assert isinstance(seq, int)
        if startDate:
            assert isinstance(startDate, date)
            query["startDate"] = startDate.strftime("%Y-%m-%d")
        if endDate:
            assert isinstance(endDate, date)
            query["endDate"] = endDate.strftime("%Y-%m-%d")

        response = self._client.get(self.url + f"({seq})/versions", query)
        data = response[self.name]
        resource_versions = [self.resource.from_dict(item) for item in data]

        return resource_versions


class _List(_Endpoint):
    def list(
        self,
        filter: str = None,  # pylint: disable=redefined-builtin
        startDate: date = None,
        endDate: date = None,
        limit: int = None,
        raw: bool = False,
        **filter_kwargs: dict,
    ) -> list[resources._Resource]:
        """
        Returns a list of resources (single valid version).

        Parameters
        ----------
        filter : str
            Add filter conditions.
        startDate : date
            Filter List for resource effective for startDate.
        endDate : date
            Filter List for resource effective for endDate.
        limit : int
            Limit the number of resources returned.
        raw : bool
            If true, then the response is returned as is, otherwise it is converted
            to resource objects. Default is False.
        filter_kwargs : dict
            Additional filter conditions, applied with the AND operator.

        Examples
        --------
        p.list()
            Returns all resources for today's effective date.
        p.list(filter="name eq '*Smith*'")
            Returns all resources with a name containing 'Smith'.
        `p.list(name="*Smith*")`
            Also returns all resources with a name containing 'Smith'.

        The keyword arguments are converted to filters. The keyword must be a
        part of the resource's attributes.
        """
        LOGGER.info("List %s", self.name)

        query = {"top": limit if limit and limit < 100 else 100}
        if expand := self.resource._expands:  # pylint: disable=protected-access
            query["expand"] = ",".join(expand)
        if filter:
            assert isinstance(filter, str)
            query["$filter"] = filter
        if startDate:
            assert isinstance(startDate, date)
            # Unlike the other methods, this one requires a date in [YYYY/MM/DD]
            query["startDate"] = startDate.strftime("%Y/%m/%d")
        if endDate:
            assert isinstance(endDate, date)
            # Unlike the other methods, this one requires a date in [YYYY/MM/DD]
            query["endDate"] = endDate.strftime("%Y/%m/%d")

        if filter_kwargs:
            filters = " and ".join([f"{k} eq '{v}'" for k, v in filter_kwargs.items()])
            if filter:
                LOGGER.warning(
                    "filter and filter_kwargs are both set,"
                    " this could lead to unexpected results."
                )
                query["$filter"] = f"({filter}) and (filters)"
            else:
                query["$filter"] = filters

        yield_count: int = 0
        response = self._client.get(self.url, query)
        data = response[self.name]
        for item in data:
            yield item if raw else self.resource.from_dict(item)
            yield_count += 1
            if limit is not None and yield_count >= limit:
                return

        while url := response.get("next"):
            response = self._client.get(url)
            data = response[self.name]
            for item in data:
                yield item if raw else self.resource.from_dict(item)
                yield_count += 1
                if limit and yield_count >= limit:
                    return

    def get_id(
        self,
        id: str,  # pylint: disable=redefined-builtin
        raw: bool = False,
    ) -> resources._Resource:
        """
        Reads all of the attributes of an existing resource.

        Parameters
        ----------
        id : str
            User unique identifier.
        raw : bool
            If true, then the response is returned as is, otherwise it is converted
            to resource objects. Default is False.
        """
        LOGGER.info("Get %s with id %s", self.name, id)

        assert isinstance(id, str)
        # pylint: disable-next=protected-access
        if (id_attr := self.resource._idAttr) is None:
            LOGGER.warning("%s has no id attribute.", self.name)
            return None

        query = {"top": 10}
        if expand := self.resource._expands:  # pylint: disable=protected-access
            query["expand"] = ",".join(expand)
        query["$filter"] = f"{id_attr} eq '{id}'"

        response = self._client.get(self.url, query)
        data = response[self.name]
        items = data if raw else [self.resource.from_dict(item) for item in data]
        if len(data) > 1:
            LOGGER.warning("Returned %s items for id %s.", len(data), id)
        item = items[0] if items else None

        return item

    def count(
        self,
        filter: str = None,  # pylint: disable=redefined-builtin
        startDate: date = None,
        endDate: date = None,
        **filter_kwargs: dict,
    ) -> int:
        """
        Returns the number of resources.

        Parameters
        ----------
        filter : str
            Add filter conditions.
        startDate : date
            Filter List for resource effective for startDate.
        endDate : date
            Filter List for resource effective for endDate.
        filter_kwargs : dict
            Additional filter conditions, applied with the AND operator.

        Examples
        --------
        p.count()
            Returns the count of resources for today's effective date.
        p.count(filter="name eq '*Smith*'")
            Returns the count of resources with a name containing 'Smith'.
        `p.count(name="*Smith*")`
            Also returns the count of resources with a name containing 'Smith'.

        The keyword arguments are converted to filters. The keyword must be a
        part of the resource's attributes.
        """
        LOGGER.info("List %s", self.name)

        query = {"top": 1, "inlineCount": True}
        if filter:
            assert isinstance(filter, str)
            query["$filter"] = filter
        if startDate:
            assert isinstance(startDate, date)
            # Unlike the other methods, this one requires a date in [YYYY/MM/DD]
            query["startDate"] = startDate.strftime("%Y/%m/%d")
        if endDate:
            assert isinstance(endDate, date)
            # Unlike the other methods, this one requires a date in [YYYY/MM/DD]
            query["endDate"] = endDate.strftime("%Y/%m/%d")

        if filter_kwargs:
            filters = " and ".join([f"{k} eq '{v}'" for k, v in filter_kwargs.items()])
            if filter:
                LOGGER.warning(
                    "filter and filter_kwargs are both set,"
                    " this could lead to unexpected results."
                )
                query["$filter"] = f"({filter}) and (filters)"
            else:
                query["$filter"] = filters

        response = self._client.get(self.url, query)
        return response["total"]


class _Update(_Endpoint):
    def update(self, update: resources._Resource) -> resources._Resource:
        """
        Update an exiting resource.

        Parameters
        ----------
        resource : resources._Resource
            Resource to update.
        """
        LOGGER.info("Update %s", self.name)

        assert isinstance(update, self.resource)
        json_data = update.to_dict()

        response = self._client.put(self.url, [json_data])
        data = response[self.name]
        updated = self.resource.from_dict(data[0])

        return updated


class _UpdateVersions(_Endpoint):
    def update_versions(self, seq: int, versions: list[resources._Resource]) -> list:
        """
        Update versions of an existing resource.

        Parameters
        ----------
        seq : int
            Resource system identifier.
        versions : list[resources._Resource]
            List of resource versions with attributes for the endpoint.
        """
        LOGGER.info("Update versions for %s with seq %s", self.name, seq)

        assert isinstance(seq, int)
        assert isinstance(versions, list)
        for version in versions:
            assert isinstance(version, self.resource)
        json_data = [item.to_dict() for item in versions]

        response = self._client.put(self.url + f"({seq})/versions", json_data)
        data = response[self.name]
        updated_versions = [self.resource.from_dict(item) for item in data]

        return updated_versions


class AppliedDeposits(_Get, _List):
    resource = resources.AppliedDeposit


class AuditLogs(_Get, _List):
    resource = resources.AuditLog


class Balances(_Get, _List):
    resource = resources.Balance


class BusinessUnits(_Create, _Get, _List, _Update):
    resource = resources.BusinessUnit


class Calendars(_Create, _Delete, _Get, _List, _Update):
    resource = resources.Calendar


class Categories(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.Category


class CategoryClassifiers(_Create, _Get, _List, _Update):
    resource = resources.CategoryClassifier


class CategoryTrees(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.CategoryTree


class Commissions(_Get, _List):
    resource = resources.Commission


class Credits(_Create, _Get, _List, _Update):
    resource = resources.Credit


class CreditTypes(_Create, _Delete, _Get, _List, _Update):
    resource = resources.CreditType


class Customers(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.Customer


class Deposits(_Create, _Get, _List, _Update):
    resource = resources.Deposit


class EarningCodes(_Create, _Delete, _Get, _List, _Update):
    resource = resources.EarningCode


class EarningGroupCodes(_Create, _Delete, _Get, _List, _Update):
    resource = resources.EarningGroupCode


class EarningGroups(_Create, _Delete, _Get, _List, _Update):
    resource = resources.EarningGroup


class EventTypes(_Create, _Delete, _Get, _List, _Update):
    resource = resources.EventType


class FixedValues(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.FixedValue


class FixedValueTypes(_Create, _Delete, _Get, _List, _Update):
    resource = resources.FixedValueType


class FixedValueVariables(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.FixedValueVariable


class Formulas(_Get, _List):
    resource = resources.Formula


class GenericClassifiers(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.GenericClassifier


class GenericClassifierTypes(_Get, _List):
    resource = resources.GenericClassifierType


class GlobalFieldNames(_Create, _Delete, _Get, _List, _Update):
    resource = resources.GlobalFieldName


class Groups(_Create, _Delete, _Get, _List, _Update):
    resource = resources.Group


class Incentives(_Get, _List):
    resource = resources.Incentive


class LookUpTables(_Get, _List):
    resource = resources.LookUpTable


class LookUpTableVariables(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.LookUpTableVariable


class Measurements(_Get, _List):
    resource = resources.Measurement


class MessageLogs(_Get, _List):
    resource = resources.MessageLog


class Messages(_Get, _List):
    resource = resources.Message


class Models(_Get, _List):
    resource = resources.Model


class Participants(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.Participant


class PaymentMappings(_Create, _Delete, _Get, _List, _Update):
    resource = resources.PaymentMapping


class Payments(_Get, _List):
    resource = resources.Payment


class PaymentSummarys(_Get, _List):
    resource = resources.PaymentSummary


class Periods(_Create, _Delete, _Get, _List, _Update):
    resource = resources.Period


class Pipelines(_Get, _List):
    resource = resources.Pipeline


class Plans(_Get, _List):
    resource = resources.Plan


class PositionGroups(_Create, _Delete, _Get, _List, _Update):
    resource = resources.PositionGroup


class PositionRelations(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.PositionRelation


class PositionRelationTypes(_Create, _Delete, _Get, _List, _Update):
    resource = resources.PositionRelationType


class Positions(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.Position


class PrimaryMeasurements(_Get, _List):
    resource = resources.PrimaryMeasurement


class ProcessingUnits(_Create, _Get, _List, _Update):
    resource = resources.ProcessingUnit


class Products(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.Product


class Quotas(_Create, _Delete, _Get, _List, _Update):
    resource = resources.Quota


class RateTables(_Get, _List):
    resource = resources.RateTable


class RateTableVariables(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.RateTableVariable


class Reasons(_Create, _Delete, _Get, _List, _Update):
    resource = resources.Reason


class SalesOrders(_Create, _Delete, _Get, _List, _Update):
    resource = resources.SalesOrder


class SalesTransactions(_Create, _Delete, _Get, _List, _Update):
    resource = resources.SalesTransaction


class SecondaryMeasurements(_Get, _List):
    resource = resources.SecondaryMeasurement


class StatusCodes(_Create, _Delete, _Get, _List, _Update):
    resource = resources.StatusCode


class Territories(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.Territory


class TerritoryVariables(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.TerritoryVariable


class Titles(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.Title


class UnitTypes(_Get, _List):
    resource = resources.UnitType


class Users(_Create, _Delete, _Get, _List, _Update):
    resource = resources.User


class Variables(
    _Create,
    _CreateVersions,
    _Delete,
    _DeleteVersions,
    _Get,
    _GetVersions,
    _List,
    _Update,
    _UpdateVersions,
):
    resource = resources.Variable
