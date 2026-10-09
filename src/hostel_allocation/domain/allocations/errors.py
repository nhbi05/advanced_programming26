"""Rule violations raised by the Allocation aggregate and its collaborators."""

from __future__ import annotations

from typing import TYPE_CHECKING

from hostel_allocation.domain.errors import DomainError

if TYPE_CHECKING:
    from hostel_allocation.domain.allocations.value_objects import AllocationNumber, StudentId


class InvalidAcademicYear(DomainError):
    """BR1: the text is not two consecutive years in "YYYY/YYYY" form."""

    def __init__(self, text: str, reason: str) -> None:
        self.text = text
        self.reason = reason
        super().__init__(reason)


class AllocationNotFound(DomainError):
    """BR6: no allocation exists with this number."""

    def __init__(self, allocation_number: AllocationNumber) -> None:
        self.allocation_number = allocation_number
        super().__init__(f"Allocation {allocation_number} was not found.")


class AllocationAlreadyCancelled(DomainError):
    """BR2: a Cancelled allocation can never be cancelled again."""

    def __init__(self, allocation_number: AllocationNumber) -> None:
        self.allocation_number = allocation_number
        super().__init__(f"Allocation {allocation_number} has already been cancelled.")


class StudentAlreadyAllocated(DomainError):
    """BR4: the student already holds an Active allocation."""

    def __init__(self, student_id: StudentId) -> None:
        self.student_id = student_id
        super().__init__(f"Student {student_id} already has an active allocation.")
