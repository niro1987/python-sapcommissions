"""Helpers for Python SAP Commissions Client."""

import asyncio
import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Union

from pydantic import BaseModel
from pydantic.fields import FieldInfo

LOGGER: logging.Logger = logging.getLogger(__name__)


@dataclass
class LogicalOperator:
    """Base class for Logical Operators.

    You cannot create a direct instance of LogicalOperator,
    use one of the subclasses instead.
    - Equals
    - NotEquals
    - GreaterThen
    - GreaterThenOrEqual
    - LesserThen
    - LesserThenOrEqual
    """

    _operator: str = field(init=False, repr=False)
    first: str
    second: str | int | date

    def __str__(self) -> str:
        """Return a string representation of the object."""
        if isinstance(self.second, int):
            second = f"{self.second}"
        elif isinstance(self.second, date):
            second = self.second.strftime("%Y-%m-%d")
        else:  # str
            second = f"'{self.second}'"

        return f"{self.first} {self._operator} {second}"


class Equals(LogicalOperator):
    """Equal to.

    Supports wildcard operator '*', for example: `Equals('name', 'John *')`.
    Supports `null` operator, for example: `Equals('name', 'null')`.
    """

    _operator: str = "eq"


class NotEquals(LogicalOperator):
    """Not equal to.

    Supports wildcard operator '*', for example: `Equals('name', 'John*')`.
    Supports `null` operator, for example: `NotEquals('name', 'null')`.
    """

    _operator: str = "ne"


class GreaterThen(LogicalOperator):
    """Greater then."""

    _operator: str = "gt"


class GreaterThenOrEqual(LogicalOperator):
    """Greater then or equals."""

    _operator: str = "ge"


class LesserThen(LogicalOperator):
    """Lesser then."""

    _operator: str = "lt"


class LesserThenOrEqual(LogicalOperator):
    """Lesser then or equals."""

    _operator: str = "le"


@dataclass(init=False)
class BooleanOperator:
    """Base class for Boolean Operators.

    You cannot create a direct instance of LogicalOperator,
    use one of the subclasses instead.
    - And
    - Or
    """

    _operator: str = field(init=False, repr=False)

    def __init__(self, *conditions: Union[LogicalOperator, "BooleanOperator"]):
        """Initialize the BooleanExpression with conditions.

        Args:
        ----
            *conditions: Instances of LogicalOperator or BooleanOperator.

        """
        if not all(
            isinstance(m, LogicalOperator | BooleanOperator)
            and type(m) not in (LogicalOperator, BooleanOperator)
            for m in conditions
        ):
            raise ValueError(
                "conditions must be instance of Boolean- or LogicalOperator"
            )
        self.conditions = conditions

    def __str__(self) -> str:
        """Return a string representation of the object."""
        if not self.conditions:
            return ""
        text: str = f" {self._operator} ".join(str(m) for m in self.conditions)
        return f"({text})" if len(self.conditions) > 1 else text


class And(BooleanOperator):
    """All conditions must be true."""

    _operator: str = "and"


class Or(BooleanOperator):
    """Any condition must be true."""

    _operator: str = "or"


class AsyncLimitedGenerator:
    """Async generator to limit the number of yielded items."""

    def __init__(self, iterable, limit: int):
        """Initialize the async iterator."""
        self.iterable = iterable
        self.limit = limit

    def __aiter__(self):
        """Return the async iterator."""
        return self

    async def __anext__(self):
        """Return the next item in the async iterator."""
        if self.limit == 0:
            raise StopAsyncIteration
        self.limit -= 1
        return await self.iterable.__anext__()


def get_alias(model_cls: type[BaseModel], field_name: str) -> str:
    """Return the alias for a field.

    Raises IndexError if field not in model.
    Raises ValueError if field does not have any alias.
    """

    model_fields: dict[str, FieldInfo] = model_cls.model_fields
    if field_name not in model_fields:
        raise IndexError(f"{field_name} not found in {model_cls.__name__}")
    model_field: FieldInfo = model_fields[field_name]
    if not model_field.alias:
        raise ValueError(f"{field_name} does not have any alias.")
    return model_field.alias


async def retry(
    coroutine_function: Callable,
    *args,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] | None = None,
    retries: int = 3,
    delay: float = 3.0,
    **kwargs,
) -> Any:
    """Retry a coroutine function a specified number of times."""
    if exceptions is not None and not isinstance(exceptions, tuple):
        exceptions = (exceptions,)

    for attempt in range(retries):
        try:
            return await coroutine_function(*args, **kwargs)
        except Exception as err:  # pylint: disable=broad-except
            if exceptions is not None and not isinstance(err, exceptions):
                raise
            LOGGER.debug("Failed attempt %s: %s", attempt + 1, err)
            if attempt >= retries - 1:
                raise
            await asyncio.sleep(delay)
