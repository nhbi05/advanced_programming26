"""The states a Borrowing can be in. See BR2 on the Borrowing aggregate root."""

from enum import Enum


class BorrowingStatus(Enum):
    """Restrict a Borrowing to exactly three states.

    A Borrowing only ever moves Requested -> Approved -> Returned, never
    backwards and never skipping a step.
    """

    REQUESTED = "Requested"
    APPROVED = "Approved"
    RETURNED = "Returned"
