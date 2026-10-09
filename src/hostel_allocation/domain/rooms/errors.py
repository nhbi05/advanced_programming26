"""Rule violations raised by the Room aggregate."""

from __future__ import annotations

from typing import TYPE_CHECKING

from hostel_allocation.domain.errors import DomainError

if TYPE_CHECKING:
    from hostel_allocation.domain.allocations.value_objects import AllocationNumber
    from hostel_allocation.domain.rooms.value_objects import Capacity, RoomNumber


class InvalidCapacity(DomainError):
    """A room's capacity fell outside the allowed range."""

    def __init__(self, value: int, maximum: int) -> None:
        self.value = value
        self.maximum = maximum
        super().__init__(
            f"A room's capacity must be between 1 and {maximum}, but got {value}."
        )


class RoomNotFound(DomainError):
    """No room exists with this number."""

    def __init__(self, room_number: RoomNumber) -> None:
        self.room_number = room_number
        super().__init__(f"Room {room_number} was not found.")


class RoomFull(DomainError):
    """BR3/BR4: the room already holds as many occupants as its capacity allows."""

    def __init__(self, room_number: RoomNumber, capacity: Capacity) -> None:
        self.room_number = room_number
        self.capacity = capacity
        super().__init__(
            f"Room {room_number} has no available capacity; "
            f"it is at its full capacity of {capacity}."
        )


class AlreadyOccupying(DomainError):
    """The same allocation was added to a room twice."""

    def __init__(self, room_number: RoomNumber, allocation_number: AllocationNumber) -> None:
        self.room_number = room_number
        self.allocation_number = allocation_number
        super().__init__(
            f"Allocation {allocation_number} already occupies room {room_number}."
        )


class NotAnOccupant(DomainError):
    """BR5: the room was asked to release an allocation it does not hold."""

    def __init__(self, room_number: RoomNumber, allocation_number: AllocationNumber) -> None:
        self.room_number = room_number
        self.allocation_number = allocation_number
        super().__init__(
            f"Room {room_number} does not have allocation "
            f"{allocation_number} as an occupant."
        )
