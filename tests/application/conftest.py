"""Wire a full, in-memory Application for use-case-level tests (T7, T8, and
general use-case coverage) -- the same composition interface/cli.py does,
just built again here so tests don't depend on the CLI.
"""

from __future__ import annotations

import pytest

from hostel_allocation.application.allocations.allocate_room import AllocateRoomService
from hostel_allocation.application.allocations.cancel_allocation import CancelAllocationService
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


class Application:
    def __init__(self) -> None:
        self.allocation_repository = InMemoryAllocationRepository()
        self.room_repository = InMemoryRoomRepository()

        eligibility_service = AllocationEligibilityService(self.allocation_repository)

        self.event_dispatcher = EventDispatcher()
        self.event_dispatcher.register(
            AllocationCancelled,
            ReleaseRoomOnAllocationCancelled(self.room_repository),
        )

        self.allocate_room = AllocateRoomService(
            self.allocation_repository, self.room_repository, eligibility_service
        )
        self.cancel_allocation = CancelAllocationService(
            self.allocation_repository, self.event_dispatcher
        )


@pytest.fixture
def app() -> Application:
    application = Application()
    application.room_repository.save(Room(RoomNumber("R-101"), Capacity(1)))
    return application
