"""Rule violations raised by the Borrowing aggregate and its collaborators."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from equipment_borrowing.domain.errors import DomainError

if TYPE_CHECKING:
    from equipment_borrowing.domain.borrowings.value_objects import BorrowingId, BorrowingStatus
    from equipment_borrowing.domain.equipment.value_objects import EquipmentId


class InvalidBorrowPeriod(DomainError):
    """BR1: the period is not 1-14 days long, or its end is not after its start."""

    def __init__(self, start: date, end: date, reason: str) -> None:
        self.start = start
        self.end = end
        self.reason = reason
        super().__init__(reason)


class InvalidBorrowState(DomainError):
    """BR2: the borrowing cannot make this move from its current status."""

    def __init__(self, borrowing_id: BorrowingId, current_status: BorrowingStatus, action: str) -> None:
        self.borrowing_id = borrowing_id
        self.current_status = current_status
        self.action = action
        super().__init__(
            f"Cannot {action} borrowing {borrowing_id} while it is {current_status.value}."
        )


class InvalidBorrowingContents(DomainError):
    """BR3: a borrowing must hold 1-3 distinct equipment items."""

    def __init__(self, equipment_ids: tuple[EquipmentId, ...], reason: str) -> None:
        self.equipment_ids = equipment_ids
        self.reason = reason
        super().__init__(reason)
