"""
Create instances of SAP Commissions objects, like `Participant` and `Credit`.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field, fields
from datetime import date, datetime, timezone
from types import UnionType
from typing import ClassVar, get_args, get_origin, get_type_hints

LOGGER = logging.getLogger(__name__)


def _decode(value, astype):
    if isinstance(value, list):
        if astype is list:
            LOGGER.error("Unknown type for list elements: %s", astype)
            raise TypeError("Unknown type for list elements: %s", astype)
        if get_origin(astype) is list:
            if len(subtypes := get_args(astype)) > 1:
                LOGGER.error("Impropper type for list elements: %s", subtypes)
                raise TypeError("Impropper type for list elements: %s", subtypes)
            return [_decode(v, subtypes[0]) for v in value]
        LOGGER.error("Impropper type, value is list: %s", astype)
        raise TypeError("Impropper type, value is list: %s", astype)
    if isinstance(astype, UnionType):
        LOGGER.error("UnionType is not supported: %s", astype)
        raise NotImplementedError("Unsupported type: %s", astype)
    if value is None:
        return None
    if astype is datetime:
        return datetime.fromisoformat(value).astimezone(timezone.utc)
    if astype is date:
        return datetime.fromisoformat(value).astimezone(timezone.utc).date()
    if isinstance(value, astype):
        return value
    if issubclass(astype, _Resource) and isinstance(value, dict):
        return astype.from_dict(value)
    if issubclass(astype, _Resource) and isinstance(value, (str, int)):
        return astype(**{astype._seq_attr: value})
    return astype(value)


def _encode(value, fromtype):
    if isinstance(value, list):
        if fromtype is list:
            LOGGER.error("Unknown type for list elements: %s", fromtype)
            raise TypeError("Unknown type for list elements: %s", fromtype)
        if get_origin(fromtype) is list:
            if len(subtypes := get_args(fromtype)) > 1:
                LOGGER.error("Impropper type for list elements: %s", subtypes)
                raise TypeError("Impropper type for list elements: %s", subtypes)
            return [_decode(v, subtypes[0]) for v in value]
        LOGGER.error("Impropper type, value is list: %s", fromtype)
        raise TypeError("Impropper type, value is list: %s", fromtype)
    if isinstance(fromtype, UnionType):
        LOGGER.error("UnionType is not supported: %s", fromtype)
        raise NotImplementedError("Unsupported type: %s", fromtype)
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    elif isinstance(value, _Resource):
        return value.to_dict(ignore_seq=False)
    if isinstance(value, int):
        return value
    return str(value)


class _Resource:
    _endpoint_name: ClassVar[str]

    @classmethod
    @property
    def _name(cls) -> str:
        """Returns the name resource."""
        return cls._endpoint_name

    @classmethod
    @property
    def _seq_attr(cls) -> str | None:
        """Returns the name of the sequence attribute or None."""
        for f in fields(cls):
            if f.metadata.get("seq"):
                return f.name

    @property
    def _seq(self) -> int | None:
        """Returns the sequence or None."""
        seq_attr = self._seq_attr
        return self[seq_attr] if seq_attr else None

    @classmethod
    @property
    def _id_attr(cls) -> str | None:
        """Returns the name of the identifier attribute or None."""
        for f in fields(cls):
            if f.metadata.get("id"):
                return f.name

    @property
    def _id(self) -> str | None:
        """Returns the identifier or None."""
        id_attr = self._id_attr
        return self[id_attr] if id_attr else None

    @classmethod
    @property
    def _expands(cls) -> tuple:
        """Returns the name of the expandable attributes."""
        return tuple(f.name for f in fields(cls) if f.metadata.get("expand"))

    @classmethod
    def from_dict(cls, json: dict) -> _Resource:
        types = get_type_hints(cls)
        invalid_json = {k: v for k, v in json.items() if k not in types.keys()}
        for field_name in invalid_json.keys():
            LOGGER.warning("%s is not a valid field for %s", field_name, cls.__name__)
        valid_json = {k: v for k, v in json.items() if k in types.keys()}
        for field_name, value in valid_json.items():
            valid_json[field_name] = _decode(value, types[field_name])
        return cls(**valid_json)

    def to_dict(self, ignore_seq: bool = True) -> dict:
        types = get_type_hints(self.__class__)
        data = {}
        for f in fields(self):
            value = self[f.name]
            if value is None:
                continue
            if f.metadata.get("json_ignore"):
                continue
            if ignore_seq and f.metadata.get("seq"):
                continue
            data[f.name] = _encode(value, types[f.name])
        return data

    def __getitem__(self, attribute: str):
        return getattr(self, attribute)


@dataclass(frozen=True)
class Error:
    message: str = field(default=None)
    timeStamp: datetime = datetime.now()


@dataclass
class Address(_Resource):
    _endpoint_name: ClassVar[str] = "address"
    address1: str = field(default=None, repr=True)
    address2: str = field(default=None, repr=False)
    address3: str = field(default=None, repr=False)
    postalCode: str = field(default=None, repr=False)
    city: str = field(default=None, repr=False)
    state: str = field(default=None, repr=False)
    country: str = field(default=None, repr=False)
    areaCode: str = field(default=None, repr=False)
    geography: str = field(default=None, repr=False)
    phone: str = field(default=None, repr=False)
    fax: str = field(default=None, repr=False)
    industry: str = field(default=None, repr=False)
    contact: str = field(default=None, repr=False)
    custId: str = field(default=None, repr=False)
    company: str = field(default=None, repr=False)


@dataclass
class AppliedDeposit(_Resource):
    _endpoint_name: ClassVar[str] = "appliedDeposits"
    appliedDepositSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    position: Position = field(default=None, repr=False)
    payee: Participant = field(default=None, repr=False)
    period: Period = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    earningGroupId: str = field(default=None, repr=False)
    earningCodeId: str = field(default=None, repr=False)
    trialPipelineRun: Pipeline = field(default=None, repr=False)
    trialPipelineRunDate: datetime = field(default=None, repr=False)
    postPipelineRun: Pipeline = field(default=None, repr=False)
    postPipelineRunDate: datetime = field(default=None, repr=False)
    entryNumber: int = field(default=None, repr=False)
    value: Value = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class AuditLog(_Resource):
    _endpoint_name: ClassVar[str] = "auditLogs"
    auditLogSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    businessUnit: BusinessUnit = field(default=None, repr=False)
    objectSeq: str = field(default=None, repr=False)
    eventDescription: str = field(default=None, repr=True)
    objectName: str = field(default=None, repr=False)
    eventType: str = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    userId: str = field(default=None, repr=False)
    eventDate: date = field(default=None, repr=False)
    objectType: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Balance(_Resource):
    _endpoint_name: ClassVar[str] = "balances"
    balanceSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    position: Position = field(default=None, repr=False)
    payee: Participant = field(default=None, repr=False)
    period: Period = field(default=None, repr=False)
    earningGroupId: str = field(default=None, repr=False)
    earningCodeId: str = field(default=None, repr=False)
    trialPipelineRun: Pipeline = field(default=None, repr=False)
    trialPipelineRunDate: datetime = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    applyPipelineRun: Pipeline = field(default=None, repr=False)
    applyPipelineRunDate: datetime = field(default=None, repr=False)
    postPipelineRun: Pipeline = field(default=None, repr=False)
    postPipelineRunDate: datetime = field(default=None, repr=False)
    balanceStatusId: str = field(default=None, repr=False)
    value: Value = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class BusinessUnit(_Resource):
    _endpoint_name: ClassVar[str] = "businessUnits"
    businessUnitSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    mask: int = field(default=None, repr=False)
    smask: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Calendar(_Resource):
    _endpoint_name: ClassVar[str] = "calendars"
    calendarSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    minorPeriodType: PeriodType = field(default=None, repr=False)
    majorPeriodType: PeriodType = field(default=None, repr=False)
    periods: Period = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Category(_Resource):
    _endpoint_name: ClassVar[str] = "categories"
    ruleElementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    owner: CategoryTree = field(default=None, repr=False)
    parent: Category = field(default=None, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    returnType: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=date(2200, 1, 1), repr=True)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createDate: datetime = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    owningElement: str = field(default=None, repr=False)
    ruleUsage: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    inputSignature: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class CategoryClassifier(_Resource):
    _endpoint_name: ClassVar[str] = "categoryClassifiers"
    categoryClassifiersSeq: int = field(
        default=None, metadata={"seq": True}, repr=False
    )
    categoryTree: CategoryTree = field(default=None, repr=False)
    category: Category = field(default=None, repr=False)
    classifier: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=date(2200, 1, 1), repr=True)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class CategoryTree(_Resource):
    _endpoint_name: ClassVar[str] = "categoryTrees"
    categoryTreeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, repr=False)
    classifierSelectorId: str = field(default=None, repr=False)
    classifierClass: str = field(default=None, repr=False)
    description: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    ruleExpression: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Commission(_Resource):
    _endpoint_name: ClassVar[str] = "commissions"
    commissionSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    position: Position = field(default=None, repr=False)
    payee: Participant = field(default=None, repr=False)
    period: Period = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    incentive: Incentive = field(default=None, repr=False)
    credit: Credit = field(default=None, repr=False)
    pipelineRun: Pipeline = field(default=None, repr=False)
    pipelineRunDate: datetime = field(default=None, repr=False)
    value: Value = field(default=None, repr=False)
    rateValue: Value = field(default=None, repr=False)
    entryNumber: str = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    isPrivate: bool = field(default=None, repr=False)
    originTypeId: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Credit(_Resource):
    _endpoint_name: ClassVar[str] = "credits"
    creditSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    payee: Participant = field(default=None, repr=False)
    position: Position = field(default=None, repr=False)
    salesOrder: SalesOrder = field(default=None, repr=False)
    salesTransaction: SalesTransaction = field(default=None, repr=False)
    period: Period = field(default=None, repr=False)
    creditType: CreditType = field(default=None, repr=False)
    value: Value = field(default=None, repr=False)
    preadjustedValue: Value = field(default=None, repr=False)
    originTypeId: str = field(default=None, repr=False)
    reason: Reason = field(default=None, repr=False)
    rule: Rule = field(default=None, repr=False)
    isRollable: bool = field(default=None, repr=False)
    rollDate: date = field(default=None, repr=False)
    isHeld: bool = field(default=None, repr=False)
    releaseDate: date = field(default=None, repr=False)
    pipelineRun: Pipeline = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    compensationDate: date = field(default=None, repr=False)
    comments: str = field(default=None, repr=False)
    pipelineRunDate: datetime = field(default=None, repr=False)
    isPrivate: bool = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class CreditType(_Resource):
    _endpoint_name: ClassVar[str] = "creditTypes"
    dataTypeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    creditTypeId: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Customer(_Resource):
    _endpoint_name: ClassVar[str] = "customers"
    classifierSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    classifierId: str = field(default=None, metadata={"id": True}, repr=True)
    name: str = field(default=None, repr=False)
    description: str = field(default=None, repr=False)
    selectorId: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    address1: str = field(default=None, repr=False)
    address2: str = field(default=None, repr=False)
    address3: str = field(default=None, repr=False)
    city: str = field(default=None, repr=False)
    state: str = field(default=None, repr=False)
    country: str = field(default=None, repr=False)
    phone: str = field(default=None, repr=False)
    areaCode: str = field(default=None, repr=False)
    postalCode: str = field(default=None, repr=False)
    geography: str = field(default=None, repr=False)
    fax: str = field(default=None, repr=False)
    email: str = field(default=None, repr=False)
    industry: str = field(default=None, repr=False)
    contact: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Deposit(_Resource):
    _endpoint_name: ClassVar[str] = "deposits"
    depositSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, repr=False)
    earningGroupId: str = field(default=None, repr=False)
    earningCodeId: str = field(default=None, repr=False)
    payee: Participant = field(default=None, repr=False)
    position: Position = field(default=None, repr=False)
    period: Period = field(default=None, repr=False)
    value: Value = field(default=None, repr=False)
    preadjustedValue: Value = field(default=None, repr=False)
    originTypeId: str = field(default=None, repr=False)
    reason: Reason = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    rule: Rule = field(default=None, repr=False)
    depositDate: date = field(default=None, repr=False)
    isHeld: bool = field(default=None, repr=False)
    releaseDate: date = field(default=None, repr=False)
    pipelineRun: Pipeline = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    comments: str = field(default=None, repr=False)
    pipelineRunDate: datetime = field(default=None, repr=False)
    isPrivate: bool = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class EarningCode(_Resource):
    _endpoint_name: ClassVar[str] = "earningCodes"
    dataTypeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    earningCodeId: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class EarningGroup(_Resource):
    _endpoint_name: ClassVar[str] = "earningGroups"
    dataTypeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    earningGroupId: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class EarningGroupCode(_Resource):
    _endpoint_name: ClassVar[str] = "earningGroupCodes"
    earningGroupCodeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    earningGroupCode: str = field(default=None, metadata={"id": True}, repr=True)
    earningCodeId: str = field(default=None, repr=False)
    earningGroupId: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class EventType(_Resource):
    _endpoint_name: ClassVar[str] = "eventTypes"
    dataTypeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    eventTypeId: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class FixedValue(_Resource):
    _endpoint_name: ClassVar[str] = "fixedValues"
    ruleElementOwnerSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    calendar: Calendar = field(default=None, repr=False)
    periodType: PeriodType = field(default=None, repr=False)
    fixedValueType: FixedValueType = field(default=None, repr=False)
    value: Value = field(default=None, repr=False)
    unitTypeSeq: UnitType = field(default=None, repr=False)
    owningElement: str = field(default=None, repr=False)
    ruleUsage: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    ruleElementSeq: str = field(default=None, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    inputSignature: str = field(default=None, repr=False)
    returnType: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class FixedValueType(_Resource):
    _endpoint_name: ClassVar[str] = "fixedValueTypes"
    dataTypeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    fixedValueTypeId: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class FixedValueVariable(_Resource):
    _endpoint_name: ClassVar[str] = "fixedValueVariables"
    ruleElementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    requiredPeriodType: PeriodType = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    defaultElement: FixedValue = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    referenceClassType: str = field(default=None, repr=False)
    returnType: str = field(default=None, repr=False)
    owningElement: str = field(default=None, repr=False)
    ruleUsage: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    inputSignature: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Formula(_Resource):
    _endpoint_name: ClassVar[str] = "formulas"
    ruleElementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    returnType: str = field(default=None, repr=False)
    owningElement: str = field(default=None, repr=False)
    ruleUsage: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    inputSignature: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class GenericClassifier(_Resource):
    _endpoint_name: ClassVar[str] = "genericClassifiers"
    classifierSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    classifierId: str = field(default=None, metadata={"id": True}, repr=True)
    name: str = field(default=None, repr=False)
    description: str = field(default=None, repr=False)
    selectorId: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class GenericClassifierType(_Resource):
    _endpoint_name: ClassVar[str] = "genericClassifierTypes"
    genericClassifierTypeSeq: int = field(
        default=None, metadata={"seq": True}, repr=False
    )
    name: str = field(default=None, metadata={"id": True}, repr=True)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class GlobalFieldName(_Resource):
    _endpoint_name: ClassVar[str] = "globalFieldNames"
    globalFieldNameSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    globalFieldNameDataTypeLength: int = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Group(_Resource):
    _endpoint_name: ClassVar[str] = "groups"
    groupSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    policy: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Incentive(_Resource):
    _endpoint_name: ClassVar[str] = "incentives"
    incentiveSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, repr=False)
    ruleElementOwnerSeq: str = field(default=None, repr=False)
    isActive: bool = field(default=None, repr=False)
    payee: Participant = field(default=None, repr=False)
    quota: Quota = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    pipelineRunDate: datetime = field(default=None, repr=False)
    value: Value = field(default=None, repr=False)
    period: Period = field(default=None, repr=False)
    releaseDate: datetime = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    attainment: str = field(default=None, repr=False)
    pipelineRun: Pipeline = field(default=None, repr=False)
    position: Position = field(default=None, repr=False)
    rule: Rule = field(default=None, repr=False)
    isPrivate: bool = field(default=None, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class LookUpTable(_Resource):
    _endpoint_name: ClassVar[str] = "relationalMDLTs"
    ruleElementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    businessUnit: BusinessUnit = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    returnType: str = field(default=None, repr=False)
    returnUnitType: UnitType = field(default=None, repr=False)
    owningElement: str = field(default=None, repr=False)
    ruleUsage: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    inputSignature: str = field(default=None, repr=False)
    treatNullAsZero: bool = field(default=None, repr=False)
    expressionTypeCounts: str = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    dimensions: LookUpTableDimension = field(
        default=None, metadata={"expand": True}, repr=False
    )
    indices: LookUpTableIndice = field(
        default=None, metadata={"expand": True}, repr=False
    )
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class LookUpTableDimension(_Resource):
    _endpoint_name: ClassVar[str] = "lookupTableDimension"
    dimensionSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    removeDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    displayOrder: int = field(default=None, repr=False)
    dimensionType: int = field(default=None, repr=False)
    dimensionSlot: int = field(default=None, repr=False)
    dimensionUnitType: UnitType = field(default=None, repr=False)
    isRanged: bool = field(default=None, repr=False)
    includeStartInRange: bool = field(default=None, repr=False)
    includeEndInRange: bool = field(default=None, repr=False)
    flags: str = field(default=None, repr=False)
    MDLT: LookUpTable = field(default=None, repr=False)
    categoryTree: CategoryTree = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class LookUpTableIndice(_Resource):
    _endpoint_name: ClassVar[str] = "lookuptableIndice"
    ordinal: int = field(default=None, repr=False)
    displayOrder: int = field(default=None, repr=False)
    minString: str = field(default=None, repr=False)
    maxString: str = field(default=None, repr=False)
    minValue: str = field(default=None, repr=False)
    maxValue: str = field(default=None, repr=False)
    minDate: date = field(default=None, repr=False)
    maxDate: date = field(default=None, repr=False)
    validStart: date = field(default=None, repr=False)
    validEnd: date = field(default=None, repr=False)
    classifier: str = field(default=None, repr=False)  # TODO Implement Classifier
    category: str = field(default=None, repr=False)  # TODO Implement Category
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    createDate: datetime = field(default=None, repr=False)
    removeDate: datetime = field(default=None, repr=False)
    MDLT: LookUpTable = field(default=None, repr=False)
    dimensionSeq: LookUpTableDimension = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class LookUpTableVariable(_Resource):
    _endpoint_name: ClassVar[str] = "lookUpTableVariables"
    ruleElementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    requiredPeriodType: PeriodType = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    defaultElement: str = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    referenceClassType: str = field(default=None, repr=False)
    returnType: str = field(default=None, repr=False)
    owningElement: str = field(default=None, repr=False)
    ruleUsage: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    inputSignature: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Measurement(_Resource):
    _endpoint_name: ClassVar[str] = "measurements"
    measurementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    position: Position = field(default=None, repr=False)
    payee: Participant = field(default=None, repr=False)
    period: Period = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    rule: Rule = field(default=None, repr=False)
    pipelineRun: Pipeline = field(default=None, repr=False)
    pipelineRunDate: datetime = field(default=None, repr=False)
    value: Value = field(default=None, repr=False)
    numberOfCredits: Value = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    isPrivate: bool = field(default=None, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class PrimaryMeasurement(_Resource):
    _endpoint_name: ClassVar[str] = "primaryMeasurements"
    measurementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    position: Position = field(default=None, repr=False)
    payee: Participant = field(default=None, repr=False)
    period: Period = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    rule: Rule = field(default=None, repr=False)
    pipelineRun: Pipeline = field(default=None, repr=False)
    pipelineRunDate: datetime = field(default=None, repr=False)
    value: Value = field(default=None, repr=False)
    numberOfCredits: Value = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    isPrivate: bool = field(default=None, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class SecondaryMeasurement(_Resource):
    _endpoint_name: ClassVar[str] = "secondaryMeasurements"
    measurementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    position: Position = field(default=None, repr=False)
    payee: Participant = field(default=None, repr=False)
    period: Period = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    rule: Rule = field(default=None, repr=False)
    pipelineRun: Pipeline = field(default=None, repr=False)
    pipelineRunDate: datetime = field(default=None, repr=False)
    value: Value = field(default=None, repr=False)
    numberOfCredits: Value = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    isPrivate: bool = field(default=None, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Message(_Resource):
    _endpoint_name: ClassVar[str] = "messages"
    messageSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    messageKey: str = field(default=None, metadata={"id": True}, repr=True)
    messageTimeStamp: datetime = field(default=None, repr=False)
    argumentCount: int = field(default=None, repr=False)
    subCategory: str = field(default=None, repr=False)
    messageLog: MessageLog = field(default=None, repr=False)
    module: str = field(default=None, repr=False)
    rule: Rule = field(default=None, repr=False)
    payee: Participant = field(default=None, repr=False)
    messageType: str = field(default=None, repr=False)
    runPeriod: Period = field(default=None, repr=False)
    objectSeq: str = field(default=None, repr=False)
    salesTransaction: SalesTransaction = field(default=None, repr=False)
    position: Position = field(default=None, repr=False)
    category: str = field(default=None, repr=False)
    credit: Credit = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class MessageLog(_Resource):
    _endpoint_name: ClassVar[str] = "messageLogs"
    messageLogSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    sourceSeq: str = field(default=None, repr=False)
    componentName: str = field(default=None, repr=False)
    logDate: datetime = field(default=None, repr=False)
    logName: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Model(_Resource):
    _endpoint_name: ClassVar[str] = "models"
    modelSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    modelName: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    status: str = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    budgetType: str = field(default=None, repr=False)
    budgetValue: Value = field(default=None, repr=False)
    useSourcePeriodAsInput: str = field(default=None, repr=False)
    sourceAdjustment: Value = field(default=None, repr=False)
    sourceStartPeriod: Period = field(default=None, repr=False)
    sourceEndPeriod: Period = field(default=None, repr=False)
    modelStartPeriod: Period = field(default=None, repr=False)
    modelEndPeriod: Period = field(default=None, repr=False)
    modificationDate: datetime = field(default=None, repr=False)
    budgetPercentValue: Value = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    useNewTransactionAsInput: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Participant(_Resource):
    _endpoint_name: ClassVar[str] = "participants"
    payeeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    payeeId: str = field(default=None, metadata={"id": True}, repr=True)
    firstName: str = field(default=None, repr=False)
    lastName: str = field(default=None, repr=False)
    middleName: str = field(default=None, repr=False)
    prefix: str = field(default=None, repr=False)
    suffix: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    hireDate: date = field(default=None, repr=False)
    terminationDate: date = field(default=None, repr=False)
    salary: Value = field(default=None, repr=False)
    userId: str = field(default=None, repr=False)
    participantEmail: str = field(default=None, repr=False)
    preferredLanguage: str = field(default=None, repr=False)
    eventCalendar: str = field(default=None, repr=False)
    taxId: str = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Payment(_Resource):
    _endpoint_name: ClassVar[str] = "payments"
    paymentSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    position: Position = field(default=None, repr=False)
    payee: Participant = field(default=None, repr=False)
    period: Period = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    earningGroupId: str = field(default=None, repr=False)
    earningCodeId: str = field(default=None, repr=False)
    trialPipelineRun: Pipeline = field(default=None, repr=False)
    trialPipelineRunDate: datetime = field(default=None, repr=False)
    postPipelineRun: Pipeline = field(default=None, repr=False)
    postPipelineRunDate: datetime = field(default=None, repr=False)
    reason: str = field(default=None, repr=False)
    value: Value = field(default=None, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class PaymentMapping(_Resource):
    _endpoint_name: ClassVar[str] = "paymentMappings"
    paymentMappingSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    sourceTableName: str = field(default=None, repr=False)
    sourceAttribute: str = field(default=None, repr=False)
    paymentAttribute: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class PaymentSummary(_Resource):
    _endpoint_name: ClassVar[str] = "paymentSummarys"
    paymentSummarySeq: int = field(default=None, metadata={"seq": True}, repr=False)
    position: Position = field(default=None, repr=False)
    participant: Participant = field(default=None, repr=False)
    period: Period = field(default=None, repr=False)
    earningGroupId: str = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    pipelineRun: Pipeline = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    pipelineRunDate: datetime = field(default=None, repr=False)
    appliedDeposit: Value = field(default=None, repr=False)
    priorBalance: Value = field(default=None, repr=False)
    balance: Value = field(default=None, repr=False)
    payment: Value = field(default=None, repr=False)
    Deposit: Value = field(default=None, repr=False)
    outstandingBalance: Value = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Period(_Resource):
    _endpoint_name: ClassVar[str] = "periods"
    periodSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    shortName: str = field(default=None, repr=False)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    periodType: PeriodType = field(default=None, repr=False)
    parent: Period = field(default=None, repr=False)
    startDate: date = field(default=None, repr=False)
    endDate: date = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class PeriodType(_Resource):
    _endpoint_name: ClassVar[str] = "periodTypes"
    periodTypeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    level: int = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Pipeline(_Resource):
    _endpoint_name: ClassVar[str] = "pipelines"
    pipelineRunSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    batchName: str = field(default=None, repr=False)
    command: str = field(default=None, repr=False)
    dateSubmitted: datetime = field(default=None, repr=False)
    description: str = field(default=None, repr=False)
    endDateScheduled: datetime = field(default=None, repr=False)
    groupName: str = field(default=None, repr=False)
    isolationLevel: str = field(default=None, repr=False)
    message: str = field(default=None, repr=False)
    modelRun: str = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    numErrors: int = field(default=None, repr=False)
    numWarnings: int = field(default=None, repr=False)
    period: str = field(default=None, repr=False)
    priority: str = field(default=None, repr=False)
    processingUnit: str = field(default=None, repr=False)
    productVersion: str = field(default=None, repr=False)
    removeDate: datetime = field(default=None, repr=False)
    reportTypeName: str = field(default=None, repr=False)
    runMode: str = field(default=None, repr=False)
    runParameters: str = field(default=None, repr=False)
    runProgress: str = field(default=None, repr=False)
    scheduleDay: str = field(default=None, repr=False)
    scheduleFrequency: str = field(default=None, repr=False)
    schemaVersion: str = field(default=None, repr=False)
    stageTables: list = field(default=None, metadata={"type": str}, repr=False)
    stageType: str = field(default=None, repr=False)
    startDateScheduled: datetime = field(default=None, repr=False)
    startTime: datetime = field(default=None, repr=False)
    state: str = field(default=None, repr=False)
    status: str = field(default=None, repr=False)
    stopTime: datetime = field(default=None, repr=False)
    storedProcVersion: str = field(default=None, repr=False)
    targetDatabase: str = field(default=None, repr=False)
    traceLevel: str = field(default=None, repr=False)
    userId: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Plan(_Resource):
    _endpoint_name: ClassVar[str] = "plans"
    ruleElementOwnerSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    variableAssignments: VariableAssignment = field(
        default=None, metadata={"expand": True}, repr=False
    )
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Position(_Resource):
    _endpoint_name: ClassVar[str] = "positions"
    ruleElementOwnerSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=date(2200, 1, 1), repr=True)
    creditStartDate: date = field(default=None, repr=False)
    creditEndDate: date = field(default=None, repr=False)
    processingStartDate: date = field(default=None, repr=False)
    processingEndDate: date = field(default=None, repr=False)
    targetCompensation: Value = field(default=None, repr=False)
    businessUnits: list[BusinessUnit] = field(default_factory=list, repr=False)
    manager: Position = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    title: Title = field(default=None, repr=False)
    positionGroup: PositionGroup = field(default=None, repr=False)
    payee: Participant = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    plan: Plan = field(default=None, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    variableAssignments: list[VariableAssignment] = field(
        default_factory=list, metadata={"expand": True}, repr=False
    )
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class PositionGroup(_Resource):
    _endpoint_name: ClassVar[str] = "positionGroups"
    positionGroupSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    businessUnits: list = field(default=None, metadata={"type": str}, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class PositionRelation(_Resource):
    _endpoint_name: ClassVar[str] = "positionRelations"
    positionRelationSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    parentPosition: Position = field(default=None, repr=False)
    positionRelationType: PositionRelationType = field(default=None, repr=False)
    childPosition: Position = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class PositionRelationType(_Resource):
    _endpoint_name: ClassVar[str] = "positionRelationTypes"
    dataTypeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    relations: PositionRelation = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class ProcessingUnit(_Resource):
    _endpoint_name: ClassVar[str] = "processingUnits"
    processingUnitSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Product(_Resource):
    _endpoint_name: ClassVar[str] = "products"
    classifierSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    classifierId: str = field(default=None, metadata={"id": True}, repr=True)
    name: str = field(default=None, repr=False)
    description: str = field(default=None, repr=False)
    selectorId: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    cost: Value = field(default=None, repr=False)
    price: Value = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Quota(_Resource):
    _endpoint_name: ClassVar[str] = "quotas"
    quotaSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, repr=False)
    description: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    businessUnit: BusinessUnit = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    unitType: UnitType = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class RateTable(_Resource):
    _endpoint_name: ClassVar[str] = "rateTables"
    ruleElementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    businessUnit: BusinessUnit = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    returnType: str = field(default=None, repr=False)
    owningElement: str = field(default=None, repr=False)
    ruleUsage: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    inputSignature: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class RateTableVariable(_Resource):
    _endpoint_name: ClassVar[str] = "rateTableVariables"
    ruleElementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    requiredPeriodType: PeriodType = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    unitType: UnitType = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    defaultElement: str = field(default=None, repr=False)
    referenceClassType: str = field(default=None, repr=False)
    returnType: str = field(default=None, repr=False)
    owningElement: str = field(default=None, repr=False)
    ruleUsage: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    inputSignature: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Reason(_Resource):
    _endpoint_name: ClassVar[str] = "reasons"
    dataTypeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    reasonId: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Rule(_Resource):
    _endpoint_name: ClassVar[str] = "rules"
    ruleSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    businessUnit: BusinessUnit = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    type: RuleType = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class RuleType(_Resource):
    _endpoint_name: ClassVar[str] = "ruleType"
    name: str = field(default=None, metadata={"id": True}, repr=True)
    id: int = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class SalesOrder(_Resource):
    _endpoint_name: ClassVar[str] = "salesOrders"
    salesOrderSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    orderId: str = field(default=None, metadata={"id": True}, repr=True)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    pipelineRun: Pipeline = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class SalesTransaction(_Resource):
    _endpoint_name: ClassVar[str] = "salesTransactions"
    salesTransactionSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    salesOrder: SalesOrder = field(default=None, repr=False)
    lineNumber: Value = field(default=None, repr=False)
    subLineNumber: Value = field(default=None, repr=False)
    value: Value = field(default=None, repr=False)
    preadjustedValue: Value = field(default=None, repr=False)
    isRunnable: bool = field(default=None, repr=False)
    compensationDate: date = field(default=None, repr=False)
    eventType: EventType = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    modificationDate: datetime = field(default=None, repr=False)
    reason: Reason = field(default=None, repr=False)
    channel: str = field(default=None, repr=False)
    poNumber: str = field(default=None, repr=False)
    dataSource: str = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    shipToAddress: Address = field(default=None, repr=False)
    otherToAddress: Address = field(default=None, repr=False)
    billToAddress: Address = field(default=None, repr=False)
    transactionAssignments: TransactionAssignment = field(
        default=None, metadata={"expand": True}, repr=False
    )
    discountType: str = field(default=None, repr=False)
    productName: str = field(default=None, repr=False)
    productDescription: str = field(default=None, repr=False)
    paymentTerms: str = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    unitValue: Value = field(default=None, repr=False)
    accountingDate: date = field(default=None, repr=False)
    discountPercent: Value = field(default=None, repr=False)
    comments: str = field(default=None, repr=False)
    productId: str = field(default=None, repr=False)
    numberOfUnits: Value = field(default=None, repr=False)
    nativeCurrencyAmount: Value = field(default=None, repr=False)
    nativeCurrency: str = field(default=None, repr=False)
    pipelineRun: Pipeline = field(default=None, repr=False)
    alternateOrderNumber: str = field(default=None, repr=False)
    originTypeId: str = field(default=None, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericAttribute17: str = field(default=None, repr=False)
    genericAttribute18: str = field(default=None, repr=False)
    genericAttribute19: str = field(default=None, repr=False)
    genericAttribute20: str = field(default=None, repr=False)
    genericAttribute21: str = field(default=None, repr=False)
    genericAttribute22: str = field(default=None, repr=False)
    genericAttribute23: str = field(default=None, repr=False)
    genericAttribute24: str = field(default=None, repr=False)
    genericAttribute25: str = field(default=None, repr=False)
    genericAttribute26: str = field(default=None, repr=False)
    genericAttribute27: str = field(default=None, repr=False)
    genericAttribute28: str = field(default=None, repr=False)
    genericAttribute29: str = field(default=None, repr=False)
    genericAttribute30: str = field(default=None, repr=False)
    genericAttribute31: str = field(default=None, repr=False)
    genericAttribute32: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class StatusCode(_Resource):
    _endpoint_name: ClassVar[str] = "statusCodes"
    dataTypeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    type: str = field(default=None, repr=False)
    isActive: bool = field(default=None, repr=False)
    status: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Territory(_Resource):
    _endpoint_name: ClassVar[str] = "territories"
    ruleElementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    definition: str = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    returnType: str = field(default=None, repr=False)
    ruleUsage: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    owningElement: str = field(default=None, repr=False)
    inputSignature: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class TerritoryVariable(_Resource):
    _endpoint_name: ClassVar[str] = "territoryVariables"
    ruleElementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: BusinessUnit = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    defaultElement: str = field(default=None, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    referenceClassType: str = field(default=None, repr=False)
    returnType: str = field(default=None, repr=False)
    owningElement: str = field(default=None, repr=False)
    ruleUsage: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    requiredPeriodType: PeriodType = field(default=None, repr=False)
    inputSignature: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Title(_Resource):
    _endpoint_name: ClassVar[str] = "titles"
    ruleElementOwnerSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: list = field(default=None, metadata={"type": str}, repr=False)
    plan: str = field(default=None, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    genericAttribute1: str = field(default=None, repr=False)
    genericAttribute2: str = field(default=None, repr=False)
    genericAttribute3: str = field(default=None, repr=False)
    genericAttribute4: str = field(default=None, repr=False)
    genericAttribute5: str = field(default=None, repr=False)
    genericAttribute6: str = field(default=None, repr=False)
    genericAttribute7: str = field(default=None, repr=False)
    genericAttribute8: str = field(default=None, repr=False)
    genericAttribute9: str = field(default=None, repr=False)
    genericAttribute10: str = field(default=None, repr=False)
    genericAttribute11: str = field(default=None, repr=False)
    genericAttribute12: str = field(default=None, repr=False)
    genericAttribute13: str = field(default=None, repr=False)
    genericAttribute14: str = field(default=None, repr=False)
    genericAttribute15: str = field(default=None, repr=False)
    genericAttribute16: str = field(default=None, repr=False)
    genericNumber1: Value = field(default=None, repr=False)
    genericNumber2: Value = field(default=None, repr=False)
    genericNumber3: Value = field(default=None, repr=False)
    genericNumber4: Value = field(default=None, repr=False)
    genericNumber5: Value = field(default=None, repr=False)
    genericNumber6: Value = field(default=None, repr=False)
    genericDate1: date = field(default=None, repr=False)
    genericDate2: date = field(default=None, repr=False)
    genericDate3: date = field(default=None, repr=False)
    genericDate4: date = field(default=None, repr=False)
    genericDate5: date = field(default=None, repr=False)
    genericDate6: date = field(default=None, repr=False)
    genericBoolean1: bool = field(default=None, repr=False)
    genericBoolean2: bool = field(default=None, repr=False)
    genericBoolean3: bool = field(default=None, repr=False)
    genericBoolean4: bool = field(default=None, repr=False)
    genericBoolean5: bool = field(default=None, repr=False)
    genericBoolean6: bool = field(default=None, repr=False)
    variableAssignments: VariableAssignment = field(
        default=None, metadata={"expand": True}, repr=False
    )
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class TransactionAssignment(_Resource):
    _endpoint_name: ClassVar[str] = "transactionAssignment"
    titleName: str = field(default=None, repr=False)
    payeeId: str = field(default=None, repr=False)
    positionName: str = field(default=None, repr=False)
    salesOrder: SalesOrder = field(default=None, repr=False)
    salesTransactionSeq: int = field(default=None, repr=False)
    setNumber: int = field(default=None, repr=False)
    compensationDate: date = field(default=None, repr=False)
    processingUnit: ProcessingUnit = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class UnitType(_Resource):
    _endpoint_name: ClassVar[str] = "unitTypes"
    unitTypeSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    symbol: str = field(default=None, repr=False)
    currencyLocale: str = field(default=None, repr=False)
    formatting: str = field(default=None, repr=False)
    positionOfSymbol: int = field(default=None, repr=False)
    reportingScale: str = field(default=None, repr=False)
    scale: int = field(default=None, repr=False)
    valueClass: dict = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class User(_Resource):
    _endpoint_name: ClassVar[str] = "users"
    userSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    id: str = field(default=None, metadata={"id": True}, repr=True)
    userName: str = field(default=None, repr=False)
    description: str = field(default=None, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    readOnlyBusinessUnitList: BusinessUnit = field(default=None, repr=False)
    fullAccessBusinessUnitList: BusinessUnit = field(default=None, repr=False)
    groups: Group = field(default=None, repr=False)
    email: str = field(default=None, repr=False)
    preferredLanguage: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Value(_Resource):
    _endpoint_name: ClassVar[str] = "value"
    value: float = field(default=None, repr=False)
    unitType: UnitType = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class Variable(_Resource):
    _endpoint_name: ClassVar[str] = "variables"
    ruleElementSeq: int = field(default=None, metadata={"seq": True}, repr=False)
    name: str = field(default=None, metadata={"id": True}, repr=True)
    description: str = field(default=None, repr=False)
    calendar: Calendar = field(default=None, repr=False)
    requiredPeriodType: PeriodType = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    businessUnits: list = field(default=None, metadata={"type": str}, repr=False)
    plan: str = field(default=None, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modifiedBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    createdBy: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
    notAllowUpdate: bool = field(default=None, repr=False)
    defaultElement: str = field(default=None, repr=False)
    referenceClassType: str = field(default=None, repr=False)
    returnType: str = field(default=None, repr=False)
    owningElement: str = field(default=None, repr=False)
    ruleUsage: str = field(default=None, metadata={"json_ignore": True}, repr=False)
    inputSignature: str = field(default=None, repr=False)
    etag: str = field(default=None, metadata={"json_ignore": True}, repr=False)


@dataclass
class VariableAssignment(_Resource):
    _endpoint_name: ClassVar[str] = "variableAssignment"
    owner: str = field(default=None, repr=False)
    variable: str = field(default=None, repr=False)
    assignment: str = field(default=None, repr=False)
    effectiveStartDate: date = field(default=None, repr=True)
    effectiveEndDate: date = field(default=None, repr=False)
    createDate: datetime = field(
        default=None, metadata={"json_ignore": True}, repr=False
    )
    modelSeq: Model = field(default=None, metadata={"json_ignore": True}, repr=False)
