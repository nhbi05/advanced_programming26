"""ApproveBorrowingService: the main use case, the one BR5's event flows from.

Flow: Request -> this Application Service -> Borrowing.approve() (Aggregate A)
-> BorrowingApproved -> EventDispatcher -> CheckOutEquipmentOnApproval
-> Equipment.check_out() (Aggregate B).

Coordination only: every rule check happens inside the domain objects it
calls; this class sequences the calls and converts domain exceptions into
outcomes.
"""

from __future__ import annotations

from equipment_borrowing.application.borrowings.borrowing_repository import BorrowingRepository
from equipment_borrowing.application.borrowings.dtos import (
    ApprovalOutcome,
    ApproveBorrowingRequest,
    ApproveBorrowingResponse,
)
from equipment_borrowing.application.event_dispatcher import EventDispatcher
from equipment_borrowing.domain.borrowings.errors import InvalidBorrowState
from equipment_borrowing.domain.borrowings.value_objects import BorrowingId
from equipment_borrowing.domain.errors import DomainError


class ApproveBorrowingService:
    """Look up a borrowing (BR6), approve it (BR2), and publish the follow-up (BR5)."""

    def __init__(
        self,
        borrowing_repository: BorrowingRepository,
        event_dispatcher: EventDispatcher,
    ) -> None:
        self._borrowing_repository = borrowing_repository
        self._event_dispatcher = event_dispatcher

    def handle(self, request: ApproveBorrowingRequest) -> ApproveBorrowingResponse:
        borrowing = self._borrowing_repository.get(BorrowingId(request.borrowing_id))  # BR6
        if borrowing is None:
            return ApproveBorrowingResponse(
                request.borrowing_id, ApprovalOutcome.BORROWING_NOT_FOUND, None
            )

        try:
            borrowing.approve()  # BR2; on success records a BorrowingApproved event
        except InvalidBorrowState:
            return ApproveBorrowingResponse(
                request.borrowing_id, ApprovalOutcome.INVALID_STATE, borrowing.status.value
            )

        self._borrowing_repository.save(borrowing)

        try:
            for event in borrowing.pull_pending_events():
                self._event_dispatcher.dispatch(event)  # BR5
        except DomainError:
            # The approval stands; only the follow-up check-out was refused.
            return ApproveBorrowingResponse(
                request.borrowing_id,
                ApprovalOutcome.APPROVED_BUT_CHECKOUT_FAILED,
                borrowing.status.value,
            )

        return ApproveBorrowingResponse(
            request.borrowing_id,
            ApprovalOutcome.APPROVED_AND_CHECKED_OUT,
            borrowing.status.value,
        )
