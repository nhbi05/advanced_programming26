"""The Capacity value object bounding how many students a Room may hold."""

from __future__ import annotations

from dataclasses import dataclass

# This named constant communicates a domain fact and avoids a magic number.
MAXIMUM_OCCUPANTS_PER_ROOM = 8


@dataclass(frozen=True, slots=True)
class Capacity:
    """A room's maximum occupant count, always between 1 and 8 inclusive."""

    value: int

    def __post_init__(self) -> None:
        """Protect the rule that a capacity must be a sane, positive number."""

        if not (1 <= self.value <= MAXIMUM_OCCUPANTS_PER_ROOM):
            raise ValueError(
                "A room's capacity must be between 1 and "
                f"{MAXIMUM_OCCUPANTS_PER_ROOM}, but got {self.value}."
            )

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)
