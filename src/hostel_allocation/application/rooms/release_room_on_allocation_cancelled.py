"""ReleaseRoomOnAllocationCancelled: the handler side of BR5.

This is deliberately in Application, not Domain: it needs a repository to
fetch Room, which is a coordination concern. The actual rule (whether the
release is accepted) still lives entirely inside Room.release_occupant().
"""

from __future__ import annotations

from hostel_allocation.domain.allocations.events import AllocationCancelled
from hostel_allocation.domain.rooms.repositories import RoomRepository


class ReleaseRoomOnAllocationCancelled:
    """Free the room space an Allocation gave up when it was cancelled."""

    def __init__(self, room_repository: RoomRepository) -> None:
        self._room_repository = room_repository

    def __call__(self, event: AllocationCancelled) -> None:
        room = self._room_repository.get(event.room_number)
        room.release_occupant(event.allocation_number)
        self._room_repository.save(room)
