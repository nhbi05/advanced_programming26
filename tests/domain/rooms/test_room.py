import pytest

from hostel_allocation.domain.allocations.value_objects import AllocationNumber
from hostel_allocation.domain.rooms.room import Room
from hostel_allocation.domain.rooms.value_objects import Capacity, RoomNumber


def new_room(capacity: int = 2) -> Room:
    return Room(RoomNumber("R-101"), Capacity(capacity))


def test_br3_a_room_accepts_occupants_up_to_its_capacity() -> None:
    # Boundary case: the second occupant brings the room to exactly capacity.
    room = new_room(capacity=2)

    room.add_occupant(AllocationNumber("ALLOC-0001"))
    room.add_occupant(AllocationNumber("ALLOC-0002"))

    assert len(room.occupants) == 2
    assert not room.has_available_capacity()


def test_br3_a_room_rejects_an_occupant_beyond_its_capacity() -> None:
    room = new_room(capacity=1)
    room.add_occupant(AllocationNumber("ALLOC-0001"))

    with pytest.raises(ValueError) as exception_info:
        room.add_occupant(AllocationNumber("ALLOC-0002"))

    assert "full capacity" in str(exception_info.value) or "capacity" in str(
        exception_info.value
    )
    assert len(room.occupants) == 1


def test_br3_releasing_a_real_occupant_frees_a_capacity_slot() -> None:
    room = new_room(capacity=1)
    allocation_number = AllocationNumber("ALLOC-0001")
    room.add_occupant(allocation_number)

    room.release_occupant(allocation_number)

    assert room.occupants == frozenset()
    assert room.has_available_capacity()


def test_t8_a_room_rejects_releasing_an_occupant_it_does_not_hold() -> None:
    # T8: Aggregate B (Room) rejects the follow-up action BR5 asks for.
    room = new_room(capacity=2)

    with pytest.raises(ValueError) as exception_info:
        room.release_occupant(AllocationNumber("ALLOC-9999"))

    assert "does not have allocation" in str(exception_info.value)
    assert room.occupants == frozenset()
