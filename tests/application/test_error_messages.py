"""User-facing wording is owned by the application layer, not the domain (SRP)."""

from __future__ import annotations

import pytest

from hostel_allocation.application.allocations.dtos import AllocateRoomRequest
from hostel_allocation.application.error_messages import _MESSAGES, describe
from hostel_allocation.domain.errors import DomainError
from hostel_allocation.domain.rooms.errors import RoomFull
from hostel_allocation.domain.rooms.value_objects import Capacity, RoomNumber


def _all_subclasses(cls: type) -> set[type]:
    direct = set(cls.__subclasses__())
    return direct.union(*(_all_subclasses(sub) for sub in direct))


def test_every_domain_error_has_a_user_message() -> None:
    import hostel_allocation.domain.allocations.errors  # noqa: F401  (register subclasses)
    import hostel_allocation.domain.rooms.errors  # noqa: F401

    missing = _all_subclasses(DomainError) - set(_MESSAGES)

    assert not missing, f"No user-facing message for: {sorted(c.__name__ for c in missing)}"


def test_describe_words_the_message_from_the_errors_facts() -> None:
    error = RoomFull(RoomNumber("R-101"), Capacity(2))

    assert describe(error) == "Room R-101 has no available capacity (all 2 places are taken)."


def test_use_case_returns_application_wording_not_domain_text(app) -> None:
    response = app.allocate_room.handle(
        AllocateRoomRequest(
            allocation_number="ALLOC-0001",
            student_id="S-1001",
            room_number="R-101",
            academic_year="2025/2027",
        )
    )

    assert response.success is False
    assert response.message == (
        '"2025/2027" is not a valid academic year. '
        'Use two consecutive years, e.g. "2025/2026".'
    )


def test_use_case_does_not_swallow_errors_that_are_not_domain_errors(app, monkeypatch) -> None:
    def broken_save(_room) -> None:
        raise ValueError("simulated bug in a repository")

    monkeypatch.setattr(app.room_repository, "save", broken_save)

    with pytest.raises(ValueError, match="simulated bug"):
        app.allocate_room.handle(
            AllocateRoomRequest(
                allocation_number="ALLOC-0001",
                student_id="S-1001",
                room_number="R-101",
                academic_year="2025/2026",
            )
        )
