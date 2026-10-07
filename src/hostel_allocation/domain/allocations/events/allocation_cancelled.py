"""The AllocationCancelled domain event. See BR5 (follow-up rule).

A domain event is a fact, named in the past tense, raised by the aggregate
whose state actually changed. It carries only plain identifiers, not live
references, so a handler must go back through a repository to act on the
aggregate the event refers to -- keeping Allocation and Room decoupled.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from hostel_allocation.domain.allocations.value_objects import AllocationNumber, StudentId
from hostel_allocation.domain.rooms.value_objects import RoomNumber


@dataclass(frozen=True, slots=True)
class AllocationCancelled:
    """Raised by Allocation.cancel() once an allocation has genuinely ended."""

    allocation_number: AllocationNumber
    room_number: RoomNumber
    student_id: StudentId
    cancelled_at: datetime
