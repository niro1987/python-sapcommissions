"""Helpers for Python SAP Commissions Client."""

from dataclasses import dataclass, field
from datetime import date
from typing import Union


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
            *conditions: Variable number of conditions that are instances of LogicalOperator or BooleanOperator.

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
