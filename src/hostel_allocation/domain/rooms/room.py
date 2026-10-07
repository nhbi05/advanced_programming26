"""The Room aggregate root.

Room is the Aggregate for BR3: the number of occupants it holds must never
exceed its Capacity. Occupants are tracked as a child collection of
AllocationNumber references -- Room never holds a live Allocation object,
only the identifier, so the two aggregates stay decoupled.
"""

from __future__ import annotations

from hostel_allocation.domain.allocations.value_objects import AllocationNumber
from hostel_allocation.domain.rooms.value_objects import Capacity, RoomNumber


class Room:
    """Guard the capacity invariant across every occupant it is given."""

    def __init__(self, room_number: RoomNumber, capacity: Capacity) -> None:
        self._room_number = room_number
        self._capacity = capacity
        self._occupants: set[AllocationNumber] = set()

    @property
    def room_number(self) -> RoomNumber:
        return self._room_number

    @property
    def capacity(self) -> Capacity:
        return self._capacity

    @property
    def occupants(self) -> frozenset[AllocationNumber]:
        """Return the current occupants as a read-only view."""

        return frozenset(self._occupants)

    def has_available_capacity(self) -> bool:
        """Return whether one more occupant could be added right now."""

        return len(self._occupants) < int(self._capacity)

    def add_occupant(self, allocation_number: AllocationNumber) -> None:
        """Record a new occupant, enforcing BR3.

        Raises ``ValueError`` when the room is already at capacity, leaving
        its occupants unchanged.
        """

        if allocation_number in self._occupants:
            raise ValueError(
                f"Allocation {allocation_number} already occupies room {self._room_number}."
            )

        if not self.has_available_capacity():
            raise ValueError(
                f"Room {self._room_number} is already at full capacity of "
                f"{self._capacity}."
            )

        self._occupants.add(allocation_number)

    def release_occupant(self, allocation_number: AllocationNumber) -> None:
        """Remove an occupant, following BR5's request from Aggregate A.

        Room only releases an occupant it actually recognises -- it does not
        trust the caller (or the event) blindly, which is what T8 verifies.
        """

        if allocation_number not in self._occupants:
            raise ValueError(
                f"Room {self._room_number} does not have allocation "
                f"{allocation_number} as an occupant."
            )

        self._occupants.discard(allocation_number)
