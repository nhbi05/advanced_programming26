import pytest

from hostel_allocation.domain.allocations.allocation import Allocation
from hostel_allocation.domain.allocations.events import AllocationCancelled
from hostel_allocation.domain.allocations.value_objects import (
    AcademicYear,
    AllocationNumber,
    AllocationStatus,
    StudentId,
)
from hostel_allocation.domain.rooms.value_objects import RoomNumber


def new_allocation() -> Allocation:
    return Allocation(
        allocation_number=AllocationNumber("ALLOC-0001"),
        student_id=StudentId("S-1001"),
        room_number=RoomNumber("R-101"),
        academic_year=AcademicYear.parse("2025/2026"),
    )


def test_br2_a_new_allocation_starts_active() -> None:
    allocation = new_allocation()

    assert allocation.status is AllocationStatus.ACTIVE


def test_br2_cancel_moves_an_active_allocation_to_cancelled() -> None:
    allocation = new_allocation()

    allocation.cancel()

    assert allocation.status is AllocationStatus.CANCELLED


def test_br2_an_already_cancelled_allocation_cannot_be_cancelled_again() -> None:
    allocation = new_allocation()
    allocation.cancel()

    with pytest.raises(ValueError) as exception_info:
        allocation.cancel()

    assert "already been cancelled" in str(exception_info.value)
    assert allocation.status is AllocationStatus.CANCELLED


def test_br5_cancelling_raises_exactly_one_allocation_cancelled_event() -> None:
    allocation = new_allocation()

    allocation.cancel()
    events = allocation.pull_pending_events()

    assert len(events) == 1
    [event] = events
    assert isinstance(event, AllocationCancelled)
    assert event.allocation_number == allocation.allocation_number
    assert event.room_number == allocation.room_number
    assert event.student_id == allocation.student_id


def test_br5_pulling_events_clears_them() -> None:
    allocation = new_allocation()
    allocation.cancel()
    allocation.pull_pending_events()

    assert allocation.pull_pending_events() == []
