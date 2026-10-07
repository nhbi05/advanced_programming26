"""AllocationEligibilityService. See BR4 (cross-concept rule).

A Domain Service because the decision needs information that does not
belong to any single entity: it must look across every other Allocation
for this student (via the repository) and ask the target Room about its
own capacity. Neither Allocation nor Room could answer this alone.
"""

from __future__ import annotations

from hostel_allocation.domain.allocations.repositories import AllocationRepository
from hostel_allocation.domain.allocations.value_objects import StudentId
from hostel_allocation.domain.rooms.room import Room


class AllocationEligibilityService:
    """Decide whether a student may be newly allocated to a room."""

    def __init__(self, allocation_repository: AllocationRepository) -> None:
        self._allocation_repository = allocation_repository

    def check(self, student_id: StudentId, room: Room) -> None:
        """Raise ``ValueError`` when the student or the room is not eligible.

        This only asks Room a question (``has_available_capacity``); it
        never inspects or duplicates Room's own BR3 invariant.
        """

        if self._allocation_repository.has_active_allocation_for(student_id):
            raise ValueError(
                f"Student {student_id} already has an active allocation."
            )

        if not room.has_available_capacity():
            raise ValueError(f"Room {room.room_number} has no available capacity.")
