import pytest

from hostel_allocation.domain.allocations.allocation import Allocation
from hostel_allocation.domain.allocations.value_objects import (
    AcademicYear,
    AllocationNumber,
    StudentId,
)
from hostel_allocation.domain.rooms.value_objects import RoomNumber
from hostel_allocation.infrastructure.allocations.in_memory_allocation_repository import (
    InMemoryAllocationRepository,
)


def test_br6_a_saved_allocation_can_be_retrieved_by_its_allocation_number() -> None:
    repository = InMemoryAllocationRepository()
    allocation = Allocation(
        AllocationNumber("ALLOC-0001"),
        StudentId("S-1001"),
        RoomNumber("R-101"),
        AcademicYear.parse("2025/2026"),
    )
    repository.save(allocation)

    found = repository.get(AllocationNumber("ALLOC-0001"))

    assert found is allocation


def test_br6_looking_up_an_unknown_allocation_number_is_rejected() -> None:
    repository = InMemoryAllocationRepository()

    with pytest.raises(ValueError) as exception_info:
        repository.get(AllocationNumber("ALLOC-9999"))

    assert "was not found" in str(exception_info.value)
