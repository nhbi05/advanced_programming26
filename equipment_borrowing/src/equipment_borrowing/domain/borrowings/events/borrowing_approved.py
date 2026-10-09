"""The BorrowingApproved domain event. See BR5 (follow-up rule).

A domain event is a fact, named in the past tense, raised by the aggregate
whose state actually changed. It carries only plain identifiers, not live
references, so a handler must go back through a repository to act on the
equipment the event refers to -- keeping Borrowing and Equipment decoupled.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from equipment_borrowing.domain.borrowings.value_objects import BorrowingId
from equipment_borrowing.domain.equipment.value_objects import EquipmentId


@dataclass(frozen=True, slots=True)
class BorrowingApproved:
    """Raised by Borrowing.approve() once a borrowing has moved to Approved."""

    borrowing_id: BorrowingId
    equipment_ids: tuple[EquipmentId, ...]
    approved_at: datetime
