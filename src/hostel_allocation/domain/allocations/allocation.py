"""The Allocation aggregate root.

An Allocation links one student to one room for one academic year. It is the
Entity/Aggregate Root for BR2: identified by its AllocationNumber, it moves
Active -> Cancelled and can never move back.
"""

from __future__ import annotations

from datetime import datetime

from hostel_allocation.domain.allocations.errors import AllocationAlreadyCancelled
from hostel_allocation.domain.allocations.events import AllocationCancelled
from hostel_allocation.domain.allocations.value_objects import (
    AcademicYear,
    AllocationNumber,
    AllocationStatus,
    StudentId,
)
from hostel_allocation.domain.rooms.value_objects import RoomNumber


class Allocation:
    """Own the Active/Cancelled lifecycle of one student-room-year link.

    Allocation has no child entities: it is the only entity in its aggregate,
    so the aggregate root and the entity are the same object.
    """

    def __init__(
        self,
        allocation_number: AllocationNumber,
        student_id: StudentId,
        room_number: RoomNumber,
        academic_year: AcademicYear,
    ) -> None:
        """Start a new allocation. Every new Allocation begins Active."""

        self._allocation_number = allocation_number
        self._student_id = student_id
        self._room_number = room_number
        self._academic_year = academic_year
        self._status = AllocationStatus.ACTIVE
        # Events raised by this aggregate wait here until an Application
        # Service pulls and dispatches them (BR5), keeping Allocation itself
        # free of any dispatching/infrastructure concern.
        self._pending_events: list[AllocationCancelled] = []

    @property
    def allocation_number(self) -> AllocationNumber:
        """Return this entity's stable identity."""

        return self._allocation_number

    @property
    def student_id(self) -> StudentId:
        return self._student_id

    @property
    def room_number(self) -> RoomNumber:
        return self._room_number

    @property
    def academic_year(self) -> AcademicYear:
        return self._academic_year

    @property
    def status(self) -> AllocationStatus:
        return self._status

    @property
    def is_active(self) -> bool:
        return self._status is AllocationStatus.ACTIVE

    def cancel(self) -> None:
        """Move this allocation to Cancelled, enforcing BR2.

        Raises ``AllocationAlreadyCancelled`` when the allocation has already been cancelled,
        leaving its state unchanged.
        """

        if self._status is AllocationStatus.CANCELLED:
            raise AllocationAlreadyCancelled(self._allocation_number)

        self._status = AllocationStatus.CANCELLED
        self._pending_events.append(
            AllocationCancelled(
                allocation_number=self._allocation_number,
                room_number=self._room_number,
                student_id=self._student_id,
                cancelled_at=datetime.now(),
            )
        )

    def pull_pending_events(self) -> list[AllocationCancelled]:
        """Return and clear the events raised since the last pull."""

        events, self._pending_events = self._pending_events, []
        return events
