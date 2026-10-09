"""The BorrowPeriod value object.

BR1 (Value rule): a borrow period lasts 1-14 days and its end falls after
its start. BorrowPeriod is the single place this is checked.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from equipment_borrowing.domain.borrowings.errors import InvalidBorrowPeriod

# This named constant communicates a domain fact and avoids a magic number.
MAXIMUM_BORROW_DAYS = 14


@dataclass(frozen=True, slots=True)
class BorrowPeriod:
    """An immutable start/end pair, defined by its value, not an identity.

    Two periods with the same dates compare as equal and are interchangeable.
    ``frozen=True`` means a period can never drift into an invalid state;
    changing a period means creating a new, validated one.
    """

    start: date
    end: date

    def __post_init__(self) -> None:
        """Protect the rule that every BorrowPeriod must be BR1-valid."""

        # end > start already guarantees the 1-day minimum.
        if self.end <= self.start:
            raise InvalidBorrowPeriod(
                self.start,
                self.end,
                f"The end date ({self.end}) must fall after the start date ({self.start}).",
            )

        if self.length_in_days > MAXIMUM_BORROW_DAYS:
            raise InvalidBorrowPeriod(
                self.start,
                self.end,
                f"A borrow period can last at most {MAXIMUM_BORROW_DAYS} days, "
                f"but this one lasts {self.length_in_days}.",
            )

    @property
    def length_in_days(self) -> int:
        return (self.end - self.start).days

    def days_late(self, returned_on: date) -> int:
        """Return how many days after the end date the equipment came back (0 if on time)."""

        return max(0, (returned_on - self.end).days)
