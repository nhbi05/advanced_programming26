"""The BorrowingId value object that identifies a Borrowing."""

from __future__ import annotations

from dataclasses import dataclass

from equipment_borrowing.domain.errors import BlankIdentifier


@dataclass(frozen=True, slots=True)
class BorrowingId:
    """A borrowing's reference, e.g. B-001."""

    value: str

    def __post_init__(self) -> None:
        """Protect the rule that a borrowing id must carry real text."""

        if not self.value.strip():
            raise BlankIdentifier("borrowing id")

    def __str__(self) -> str:
        return self.value
