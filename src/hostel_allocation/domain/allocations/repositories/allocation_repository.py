"""The AllocationRepository contract. See BR6 (lookup rule).

Only the abstract contract lives here; the in-memory implementation used at
runtime is in infrastructure/allocations/in_memory_allocation_repository.py.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from hostel_allocation.domain.allocations.allocation import Allocation
from hostel_allocation.domain.allocations.value_objects import AllocationNumber, StudentId


class AllocationRepository(ABC):
    """Persist and retrieve Allocation aggregates by their identity."""

    @abstractmethod
    def save(self, allocation: Allocation) -> None:
        """Store an allocation, replacing any previous version of it."""

    @abstractmethod
    def get(self, allocation_number: AllocationNumber) -> Allocation:
        """Return the allocation with this number.

        Raises ``AllocationNotFound`` when no such allocation exists -- this is the
        check housing staff rely on before cancelling an allocation (BR6).
        """

    @abstractmethod
    def has_active_allocation_for(self, student_id: StudentId) -> bool:
        """Return whether this student already holds an Active allocation.

        Used by AllocationEligibilityService (BR4) -- a cross-aggregate
        query, not something a single Allocation instance could answer.
        """
