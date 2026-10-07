from hostel_allocation.application.allocations.dtos import (
    AllocateRoomRequest,
    CancelAllocationRequest,
)
from hostel_allocation.domain.allocations.value_objects import AllocationNumber, AllocationStatus
from hostel_allocation.domain.rooms.value_objects import RoomNumber


def test_t7_cancelling_an_allocation_releases_the_room_and_updates_aggregate_b(app) -> None:
    # T7: successful main use case. Verifies the AllocationCancelled event is
    # handled and Room (Aggregate B) changes as expected.
    app.allocate_room.handle(
        AllocateRoomRequest("ALLOC-0001", "S-1001", "R-101", "2025/2026")
    )

    response = app.cancel_allocation.handle(
        CancelAllocationRequest(allocation_number="ALLOC-0001")
    )

    assert response.success is True

    allocation = app.allocation_repository.get(AllocationNumber("ALLOC-0001"))
    assert allocation.status is AllocationStatus.CANCELLED

    room = app.room_repository.get(RoomNumber("R-101"))
    assert room.occupants == frozenset()
    assert room.has_available_capacity()


def test_t7_a_freed_room_can_then_be_allocated_to_another_student(app) -> None:
    app.allocate_room.handle(
        AllocateRoomRequest("ALLOC-0001", "S-1001", "R-101", "2025/2026")
    )
    app.cancel_allocation.handle(CancelAllocationRequest("ALLOC-0001"))

    second_response = app.allocate_room.handle(
        AllocateRoomRequest("ALLOC-0002", "S-2002", "R-101", "2025/2026")
    )

    assert second_response.success is True


def test_cancelling_an_unknown_allocation_number_is_rejected(app) -> None:
    response = app.cancel_allocation.handle(CancelAllocationRequest("ALLOC-9999"))

    assert response.success is False
    assert "was not found" in response.message


def test_cancelling_an_already_cancelled_allocation_is_rejected(app) -> None:
    app.allocate_room.handle(
        AllocateRoomRequest("ALLOC-0001", "S-1001", "R-101", "2025/2026")
    )
    app.cancel_allocation.handle(CancelAllocationRequest("ALLOC-0001"))

    response = app.cancel_allocation.handle(CancelAllocationRequest("ALLOC-0001"))

    assert response.success is False
    assert "already been cancelled" in response.message
