"""The StudentId value object that identifies the student in an Allocation."""

from __future__ import annotations

from dataclasses import dataclass

from hostel_allocation.domain.errors import BlankIdentifier


@dataclass(frozen=True, slots=True)
class StudentId:
    """A student's registration number, e.g. S-1001.

    The hostel domain does not own student records, so a Student is never
    modelled as its own entity here -- only this identifier crosses the
    boundary into the Allocation aggregate.
    """

    value: str

    def __post_init__(self) -> None:
        """Protect the rule that a student id must carry real text."""

        if not self.value.strip():
            raise BlankIdentifier("student id")

    def __str__(self) -> str:
        return self.value
