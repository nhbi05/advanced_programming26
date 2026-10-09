"""The Borrowing aggregate root (Aggregate A).

A Borrowing is a request to borrow one to three equipment items for a
period. It is the Entity/Aggregate Root for:

- BR2 (State rule): identified by its BorrowingId, it moves only
  Requested -> Approved -> Returned.
- BR3 (Invariant rule): it holds 1-3 distinct equipment items.

Borrowing refers to equipment by EquipmentId only, never by holding a live
Equipment object, so the two aggregates stay decoupled.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Iterable

from equipment_borrowing.domain.borrowings.errors import (
    InvalidBorrowingContents,
    InvalidBorrowState,
)
from equipment_borrowing.domain.borrowings.events import BorrowingApproved
from equipment_borrowing.domain.borrowings.value_objects import (
    BorrowingId,
    BorrowingStatus,
    BorrowPeriod,
)
from equipment_borrowing.domain.equipment.value_objects import EquipmentId

MAXIMUM_ITEMS_PER_BORROWING = 3


class Borrowing:
    """Own the lifecycle and contents of one request to borrow equipment.

    Borrowing has no child entities: it is the only entity in its aggregate,
    so the aggregate root and the entity are the same object.
    """

    def __init__(
        self,
        borrowing_id: BorrowingId,
        period: BorrowPeriod,
        equipment_ids: Iterable[EquipmentId],
    ) -> None:
        """Start a new borrowing. Every new Borrowing begins Requested."""

        contents = tuple(equipment_ids)
        self._check_contents(contents)  # BR3

        self._borrowing_id = borrowing_id
        self._period = period
        self._equipment_ids = contents
        self._status = BorrowingStatus.REQUESTED
        # Events raised by this aggregate wait here until an Application
        # Service pulls and dispatches them (BR5), keeping Borrowing itself
        # free of any dispatching/infrastructure concern.
        self._pending_events: list[BorrowingApproved] = []

    @property
    def borrowing_id(self) -> BorrowingId:
        """Return this entity's stable identity."""

        return self._borrowing_id

    @property
    def period(self) -> BorrowPeriod:
        return self._period

    @property
    def equipment_ids(self) -> tuple[EquipmentId, ...]:
        """Return the equipment held as a read-only tuple."""

        return self._equipment_ids

    @property
    def status(self) -> BorrowingStatus:
        return self._status

    def add_equipment(self, equipment_id: EquipmentId) -> None:
        """Add one more item while the borrowing is still Requested (BR2, BR3).

        Raises ``InvalidBorrowingContents`` when the item would be a fourth or
        a duplicate, leaving the contents unchanged.
        """

        self._require_status(BorrowingStatus.REQUESTED, "add equipment to")
        contents = self._equipment_ids + (equipment_id,)
        self._check_contents(contents)
        self._equipment_ids = contents

    def approve(self) -> None:
        """Move this borrowing Requested -> Approved, enforcing BR2.

        Raises ``InvalidBorrowState`` from any other status, leaving the
        borrowing unchanged -- so it can never be approved twice.
        """

        self._require_status(BorrowingStatus.REQUESTED, "approve")

        self._status = BorrowingStatus.APPROVED
        self._pending_events.append(
            BorrowingApproved(
                borrowing_id=self._borrowing_id,
                equipment_ids=self._equipment_ids,
                approved_at=datetime.now(),
            )
        )

    def mark_returned(self) -> None:
        """Move this borrowing Approved -> Returned, enforcing BR2."""

        self._require_status(BorrowingStatus.APPROVED, "return")
        self._status = BorrowingStatus.RETURNED

    def days_late(self, returned_on: date) -> int:
        """Return how many days late the equipment is if it comes back on this date."""

        return self._period.days_late(returned_on)

    def pull_pending_events(self) -> list[BorrowingApproved]:
        """Return and clear the events raised since the last pull."""

        events, self._pending_events = self._pending_events, []
        return events

    def _require_status(self, expected: BorrowingStatus, action: str) -> None:
        if self._status is not expected:
            raise InvalidBorrowState(self._borrowing_id, self._status, action)

    @staticmethod
    def _check_contents(equipment_ids: tuple[EquipmentId, ...]) -> None:
        """Protect BR3: 1-3 items, never the same item twice."""

        if not 1 <= len(equipment_ids) <= MAXIMUM_ITEMS_PER_BORROWING:
            raise InvalidBorrowingContents(
                equipment_ids,
                f"A borrowing must hold 1 to {MAXIMUM_ITEMS_PER_BORROWING} equipment "
                f"items, but got {len(equipment_ids)}.",
            )

        if len(set(equipment_ids)) != len(equipment_ids):
            raise InvalidBorrowingContents(
                equipment_ids, "A borrowing cannot hold the same equipment item twice."
            )
