"""Input and output DTOs for the Approve Borrowing use case.

DTOs cross the Application Service boundary as plain data -- callers never
pass or receive domain objects (Borrowing, Equipment, value objects) directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ApprovalOutcome(Enum):
    APPROVED_AND_CHECKED_OUT = "APPROVED_AND_CHECKED_OUT"
    APPROVED_BUT_CHECKOUT_FAILED = "APPROVED_BUT_CHECKOUT_FAILED"
    BORROWING_NOT_FOUND = "BORROWING_NOT_FOUND"
    INVALID_STATE = "INVALID_STATE"


@dataclass(frozen=True, slots=True)
class ApproveBorrowingRequest:
    borrowing_id: str


@dataclass(frozen=True, slots=True)
class ApproveBorrowingResponse:
    borrowing_id: str
    outcome: ApprovalOutcome
    status: str | None
