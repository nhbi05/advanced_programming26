"""The minimal entry point: a demo scenario run against the wired application.

Wiring lives in interface/composition.py; this module only seeds sample data
and calls use cases. No business rule is implemented here.
"""

from __future__ import annotations

from hostel_allocation.application.allocations.dtos import (
    AllocateRoomRequest,
    CancelAllocationRequest,
)
from hostel_allocation.domain.rooms.room import Room
from hostel_allocation.domain.rooms.value_objects import Capacity, RoomNumber
from hostel_allocation.interface.composition import build_application


def main() -> None:
    app = build_application()

    app.room_repository.save(Room(RoomNumber("R-101"), Capacity(2)))

    allocation_response = app.allocate_room.handle(
        AllocateRoomRequest(
            allocation_number="ALLOC-0001",
            student_id="S-1001",
            room_number="R-101",
            academic_year="2025/2026",
        )
    )
    print(allocation_response)

    cancel_response = app.cancel_allocation.handle(
        CancelAllocationRequest(allocation_number="ALLOC-0001")
    )
    print(cancel_response)

    second_allocation_response = app.allocate_room.handle(
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
