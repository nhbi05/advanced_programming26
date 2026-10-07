"""CancelAllocationService: the second use case, the one BR5's event flows from.

Flow: Request -> this Application Service -> Allocation.cancel() (Aggregate A)
-> AllocationCancelled -> EventDispatcher -> ReleaseRoomOnAllocationCancelled
-> Room.release_occupant() (Aggregate B).
"""

from __future__ import annotations

from hostel_allocation.application.allocations.dtos import (
    CancelAllocationRequest,
    CancelAllocationResponse,
)
from hostel_allocation.application.event_dispatcher import EventDispatcher
from hostel_allocation.domain.allocations.repositories import AllocationRepository
from hostel_allocation.domain.allocations.value_objects import AllocationNumber


class CancelAllocationService:
    """Look up an allocation (BR6), cancel it (BR2), and publish the follow-up (BR5)."""

    def __init__(
        self,
        allocation_repository: AllocationRepository,
        event_dispatcher: EventDispatcher,
    ) -> None:
        self._allocation_repository = allocation_repository
        self._event_dispatcher = event_dispatcher

    def handle(self, request: CancelAllocationRequest) -> CancelAllocationResponse:
        try:
            allocation = self._allocation_repository.get(  # BR6
                AllocationNumber(request.allocation_number)
            )
            allocation.cancel()  # BR2, raises AllocationCancelled internally
            self._allocation_repository.save(allocation)
        except ValueError as error:
            return CancelAllocationResponse(success=False, message=str(error))

        for event in allocation.pull_pending_events():
            self._event_dispatcher.dispatch(event)  # BR5

        return CancelAllocationResponse(success=True, message="Allocation cancelled.")
