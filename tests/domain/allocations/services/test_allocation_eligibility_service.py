import pytest

from hostel_allocation.domain.allocations.allocation import Allocation
from hostel_allocation.domain.allocations.services import AllocationEligibilityService
from hostel_allocation.domain.allocations.value_objects import (
    AcademicYear,
    AllocationNumber,
    StudentId,
)
from hostel_allocation.domain.rooms.room import Room
from hostel_allocation.domain.rooms.value_objects import Capacity, RoomNumber
from hostel_allocation.infrastructure.allocations.in_memory_allocation_repository import (
    InMemoryAllocationRepository,
)


def test_br4_a_student_with_an_active_allocation_is_not_eligible_for_another() -> None:
    allocation_repository = InMemoryAllocationRepository()
    student_id = StudentId("S-1001")
    allocation_repository.save(
        Allocation(
            AllocationNumber("ALLOC-0001"),
            student_id,
            RoomNumber("R-101"),
            AcademicYear.parse("2025/2026"),
        )
    )
    service = AllocationEligibilityService(allocation_repository)
    room = Room(RoomNumber("R-102"), Capacity(2))

    with pytest.raises(ValueError) as exception_info:
        service.check(student_id, room)

    assert "already has an active allocation" in str(exception_info.value)


def test_br4_a_full_room_is_not_eligible_regardless_of_the_student() -> None:
    allocation_repository = InMemoryAllocationRepository()
    service = AllocationEligibilityService(allocation_repository)
    room = Room(RoomNumber("R-101"), Capacity(1))
    room.add_occupant(AllocationNumber("ALLOC-9999"))

    with pytest.raises(ValueError) as exception_info:
        service.check(StudentId("S-2002"), room)

    assert "no available capacity" in str(exception_info.value)


def test_br4_a_student_without_an_active_allocation_and_a_room_with_space_is_eligible() -> None:
    allocation_repository = InMemoryAllocationRepository()
    service = AllocationEligibilityService(allocation_repository)
    room = Room(RoomNumber("R-101"), Capacity(2))

    service.check(StudentId("S-3003"), room)  # does not raise
