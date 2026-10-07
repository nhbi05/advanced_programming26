"""The in-memory AllocationRepository implementation used for this coursework.

No database is required by the brief; a plain dict is the whole persistence
mechanism, supplied to Application Services via dependency injection at the
composition root (interface/cli.py).
"""

from __future__ import annotations

from hostel_allocation.domain.allocations.allocation import Allocation
from hostel_allocation.domain.allocations.repositories import AllocationRepository
from hostel_allocation.domain.allocations.value_objects import AllocationNumber, StudentId


class InMemoryAllocationRepository(AllocationRepository):
    def __init__(self) -> None:
        self._allocations: dict[AllocationNumber, Allocation] = {}

    def save(self, allocation: Allocation) -> None:
        self._allocations[allocation.allocation_number] = allocation

    def get(self, allocation_number: AllocationNumber) -> Allocation:
        try:
            return self._allocations[allocation_number]
        except KeyError as error:
            raise ValueError(f"Allocation {allocation_number} was not found.") from error

    def has_active_allocation_for(self, student_id: StudentId) -> bool:
        return any(
            allocation.student_id == student_id and allocation.is_active
            for allocation in self._allocations.values()
        )
