"""The AllocationNumber value object that identifies an Allocation."""

from __future__ import annotations

from dataclasses import dataclass

from hostel_allocation.domain.errors import BlankIdentifier


@dataclass(frozen=True, slots=True)
class AllocationNumber:
    """The reference housing staff use to find an allocation, e.g. ALLOC-0001.

    This is a value object used as an identifier: AllocationNumber has no
    identity of its own -- two instances holding the same text are equal --
    but Allocation uses one to give itself identity (BR2). ``frozen=True``
    keeps the text from ever changing after construction.
    """

    value: str

    def __post_init__(self) -> None:
        """Protect the rule that an allocation number must carry real text."""

        if not self.value.strip():
            raise BlankIdentifier("allocation number")

    def __str__(self) -> str:
        return self.value
