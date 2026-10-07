"""The AcademicYear value object used to schedule a hostel Allocation.

BR1 (Value rule): an academic year is only valid as two consecutive calendar
years, e.g. "2025/2026". AcademicYear is the single place this is checked.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AcademicYear:
    """An immutable pair of consecutive years, defined by its value, not an identity.

    Two AcademicYear instances with the same years compare as equal, and
    ``frozen=True`` means an AcademicYear can never drift into an invalid state
    after construction.
    """

    start_year: int
    end_year: int

    def __post_init__(self) -> None:
        """Protect the rule that every AcademicYear must be BR1-valid."""

        if self.end_year != self.start_year + 1:
            raise ValueError(
                "An academic year must span two consecutive years, "
                f"but got {self.start_year}/{self.end_year}."
            )

    @classmethod
    def parse(cls, text: str) -> AcademicYear:
        """Parse the "YYYY/YYYY" form staff and students actually type."""

        parts = text.split("/")
        if len(parts) != 2 or not all(part.isdigit() for part in parts):
            raise ValueError(
                f'An academic year must look like "2025/2026", but got "{text}".'
            )

        start_year, end_year = (int(part) for part in parts)
        return cls(start_year, end_year)

    def __str__(self) -> str:
        return f"{self.start_year}/{self.end_year}"
