"""The minimal entry point. It only wires dependencies and calls use cases --
no business rule is implemented here.
"""

from __future__ import annotations

from hostel_allocation.application.allocations.allocate_room import AllocateRoomService
from hostel_allocation.application.allocations.cancel_allocation import CancelAllocationService
from hostel_allocation.application.allocations.dtos import (
    AllocateRoomRequest,
    CancelAllocationRequest,
)
from hostel_allocation.application.event_dispatcher import EventDispatcher
from hostel_allocation.application.rooms.release_room_on_allocation_cancelled import (
    ReleaseRoomOnAllocationCancelled,
)
from hostel_allocation.domain.allocations.events import AllocationCancelled
from hostel_allocation.domain.allocations.services import AllocationEligibilityService
from hostel_allocation.domain.rooms.room import Room
from hostel_allocation.domain.rooms.value_objects import Capacity, RoomNumber
from hostel_allocation.infrastructure.allocations.in_memory_allocation_repository import (
    InMemoryAllocationRepository,
)
from hostel_allocation.infrastructure.rooms.in_memory_room_repository import (
    InMemoryRoomRepository,
)


def main() -> None:
    # Composition root: repository implementations are built here and
    # injected into the Application Services from outside.
    allocation_repository = InMemoryAllocationRepository()
    room_repository = InMemoryRoomRepository()

    eligibility_service = AllocationEligibilityService(allocation_repository)

    event_dispatcher = EventDispatcher()
    event_dispatcher.register(
        AllocationCancelled,
        ReleaseRoomOnAllocationCancelled(room_repository),
    )

    allocate_room = AllocateRoomService(
        allocation_repository, room_repository, eligibility_service
    )
    cancel_allocation = CancelAllocationService(allocation_repository, event_dispatcher)

    room_repository.save(Room(RoomNumber("R-101"), Capacity(2)))

    allocation_response = allocate_room.handle(
        AllocateRoomRequest(
            allocation_number="ALLOC-0001",
            student_id="S-1001",
            room_number="R-101",
            academic_year="2025/2026",
        )
    )
    print(allocation_response)

    cancel_response = cancel_allocation.handle(
        CancelAllocationRequest(allocation_number="ALLOC-0001")
    )
    print(cancel_response)

    second_allocation_response = allocate_room.handle(
        AllocateRoomRequest(
            allocation_number="ALLOC-0002",
            student_id="S-2002",
            room_number="R-101",
            academic_year="2025/2026",
        )
    )
    print(second_allocation_response)


if __name__ == "__main__":
    main()
