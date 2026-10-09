"""The wording housing staff see when a use case is refused.

This is the single place user-facing text is chosen. Domain errors only
report *what* went wrong (as typed attributes); rewording or translating a
message changes this file and never touches Room, Allocation or any other
domain object.
"""

from __future__ import annotations

from typing import Callable

from hostel_allocation.domain.allocations.errors import (
    AllocationAlreadyCancelled,
    AllocationNotFound,
    InvalidAcademicYear,
    StudentAlreadyAllocated,
)
from hostel_allocation.domain.errors import BlankIdentifier, DomainError
from hostel_allocation.domain.rooms.errors import (
    AlreadyOccupying,
    InvalidCapacity,
    NotAnOccupant,
    RoomFull,
    RoomNotFound,
)

_MESSAGES: dict[type[DomainError], Callable] = {
    BlankIdentifier: lambda e: f"Please enter a {e.identifier_name}.",
    InvalidAcademicYear: lambda e: (
        f'"{e.text}" is not a valid academic year. '
        'Use two consecutive years, e.g. "2025/2026".'
    ),
    AllocationNotFound: lambda e: f"Allocation {e.allocation_number} was not found.",
    AllocationAlreadyCancelled: lambda e: (
        f"Allocation {e.allocation_number} has already been cancelled."
    ),
    StudentAlreadyAllocated: lambda e: (
        f"Student {e.student_id} already has a room this academic year."
    ),
    InvalidCapacity: lambda e: f"A room must hold between 1 and {e.maximum} students.",
    RoomNotFound: lambda e: f"Room {e.room_number} was not found.",
    RoomFull: lambda e: (
        f"Room {e.room_number} has no available capacity "
        f"(all {e.capacity} places are taken)."
    ),
    AlreadyOccupying: lambda e: (
        f"Allocation {e.allocation_number} is already in room {e.room_number}."
    ),
    NotAnOccupant: lambda e: (
        f"Allocation {e.allocation_number} is not in room {e.room_number}."
    ),
}


def describe(error: DomainError) -> str:
    """Return the user-facing message for a refused operation."""

    message = _MESSAGES.get(type(error))
    return message(error) if message else str(error)
