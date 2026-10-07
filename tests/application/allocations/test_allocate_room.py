from hostel_allocation.application.allocations.dtos import AllocateRoomRequest


def test_allocating_a_room_succeeds_for_an_eligible_student(app) -> None:
    response = app.allocate_room.handle(
        AllocateRoomRequest("ALLOC-0001", "S-1001", "R-101", "2025/2026")
    )

    assert response.success is True
    assert response.allocation_number == "ALLOC-0001"


def test_allocating_a_room_fails_once_the_room_is_full(app) -> None:
    app.allocate_room.handle(
        AllocateRoomRequest("ALLOC-0001", "S-1001", "R-101", "2025/2026")
    )

    response = app.allocate_room.handle(
        AllocateRoomRequest("ALLOC-0002", "S-2002", "R-101", "2025/2026")
    )

    assert response.success is False
    assert "no available capacity" in response.message


def test_allocating_a_room_fails_for_an_invalid_academic_year(app) -> None:
    response = app.allocate_room.handle(
        AllocateRoomRequest("ALLOC-0001", "S-1001", "R-101", "2025-2026")
    )

    assert response.success is False
