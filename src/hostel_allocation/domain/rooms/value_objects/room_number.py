"""The RoomNumber value object that identifies a Room."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RoomNumber:
    """A room's printed identifier, e.g. R-101, used as Room's identity.

    Like AllocationNumber, this is a value object rather than an entity --
    two RoomNumbers with the same text are equal -- but Room relies on one
    to be found and compared by identity elsewhere in the model.
    """

    value: str

    def __post_init__(self) -> None:
        """Protect the rule that a room number must carry real text."""

        if not self.value.strip():
            raise ValueError("A room number cannot be blank.")

    def __str__(self) -> str:
        return self.value
