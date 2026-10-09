"""The composition root: the one place concrete implementations are chosen.

This module only builds and connects objects -- it seeds no data and runs no
scenario. Swapping the in-memory repositories for real ones, or registering
another event handler, changes this file and nothing else. Every entry point
(the CLI, the tests) gets a fully wired application from build_application().
"""

from __future__ import annotations

from dataclasses import dataclass

from hostel_allocation.application.allocations.allocate_room import AllocateRoomService
from hostel_allocation.application.allocations.cancel_allocation import CancelAllocationService
from hostel_allocation.application.event_dispatcher import EventDispatcher
from hostel_allocation.application.rooms.release_room_on_allocation_cancelled import (
    ReleaseRoomOnAllocationCancelled,
)
from hostel_allocation.domain.allocations.events import AllocationCancelled
from hostel_allocation.domain.allocations.repositories import AllocationRepository
from hostel_allocation.domain.allocations.services import AllocationEligibilityService
from hostel_allocation.domain.rooms.repositories import RoomRepository
from hostel_allocation.infrastructure.allocations.in_memory_allocation_repository import (
    InMemoryAllocationRepository,
)
from hostel_allocation.infrastructure.rooms.in_memory_room_repository import (
    InMemoryRoomRepository,
)


@dataclass(frozen=True)
class Application:
    """The wired use cases, plus the repositories behind them."""

    allocation_repository: AllocationRepository
    room_repository: RoomRepository
    allocate_room: AllocateRoomService
    cancel_allocation: CancelAllocationService


def build_application() -> Application:
    allocation_repository = InMemoryAllocationRepository()
    room_repository = InMemoryRoomRepository()

    eligibility_service = AllocationEligibilityService(allocation_repository)

    event_dispatcher = EventDispatcher()
    event_dispatcher.register(
        AllocationCancelled,
        ReleaseRoomOnAllocationCancelled(room_repository),
    )

    return Application(
        allocation_repository=allocation_repository,
        room_repository=room_repository,
        allocate_room=AllocateRoomService(
            allocation_repository, room_repository, eligibility_service
        ),
        cancel_allocation=CancelAllocationService(allocation_repository, event_dispatcher),
    )
