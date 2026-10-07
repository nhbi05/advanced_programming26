"""The states an Allocation can be in. See BR2 on the Allocation aggregate root."""

from enum import Enum


class AllocationStatus(Enum):
    """Restrict an Allocation to exactly two states: Active and Cancelled.

    Using an enum, rather than a plain string, means no other status value
    can ever enter the domain, and Allocation.cancel() can compare against a
    named member instead of a magic string. An Allocation only ever moves
    Active -> Cancelled, never back.
    """

    ACTIVE = "Active"
    CANCELLED = "Cancelled"
