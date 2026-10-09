"""Provide a full, in-memory Application for use-case-level tests (T7, T8, and
general use-case coverage) -- built by the same composition root the CLI
uses, so tests exercise the real wiring rather than a copy of it.
"""

from __future__ import annotations

import pytest

from hostel_allocation.domain.rooms.room import Room
from hostel_allocation.domain.rooms.value_objects import Capacity, RoomNumber
from hostel_allocation.interface.composition import Application, build_application


@pytest.fixture
def app() -> Application:
    application = build_application()
    application.room_repository.save(Room(RoomNumber("R-101"), Capacity(1)))
    return application
