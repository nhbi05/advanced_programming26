"""The BorrowingRepository contract. See BR6 (lookup rule).

Abstractions are defined in the layer that uses them. No domain object or
domain service needs to look up a Borrowing -- only ApproveBorrowingService
does -- so this contract lives in Application, shaped to that service's
needs. Infrastructure implements it
(infrastructure/borrowings/in_memory_borrowing_repository.py), so the
dependency still points inward.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from equipment_borrowing.domain.borrowings.borrowing import Borrowing
from equipment_borrowing.domain.borrowings.value_objects import BorrowingId


class BorrowingRepository(ABC):
    """Persist and retrieve Borrowing aggregates by their identity."""

    @abstractmethod
    def save(self, borrowing: Borrowing) -> None:
        """Store a borrowing, replacing any previous version of it."""

    @abstractmethod
    def get(self, borrowing_id: BorrowingId) -> Borrowing | None:
        """Return the borrowing with this id, or None when it does not exist.

        This is the check ApproveBorrowingService relies on before approving (BR6).
        """
