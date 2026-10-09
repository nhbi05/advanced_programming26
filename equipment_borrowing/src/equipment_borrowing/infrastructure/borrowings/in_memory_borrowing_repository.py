"""The in-memory BorrowingRepository implementation used for this coursework.

No database is required by the brief; a plain dict is the whole persistence
mechanism, supplied to Application Services via dependency injection at the
composition root (interface/composition.py).
"""

from __future__ import annotations

from equipment_borrowing.application.borrowings.borrowing_repository import BorrowingRepository
from equipment_borrowing.domain.borrowings.borrowing import Borrowing
from equipment_borrowing.domain.borrowings.value_objects import BorrowingId


class InMemoryBorrowingRepository(BorrowingRepository):
    def __init__(self) -> None:
        self._borrowings: dict[BorrowingId, Borrowing] = {}

    def save(self, borrowing: Borrowing) -> None:
        self._borrowings[borrowing.borrowing_id] = borrowing

    def get(self, borrowing_id: BorrowingId) -> Borrowing | None:
        return self._borrowings.get(borrowing_id)
