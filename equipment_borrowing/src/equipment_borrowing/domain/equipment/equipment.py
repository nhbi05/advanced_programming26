"""The Equipment aggregate root (Aggregate B).

Equipment is one specific physical item, such as one projector. Its
invariant: it can be checked out only while it is Available (BR5). The
borrowing holding it is tracked as a BorrowingId reference -- Equipment
never holds a live Borrowing object, so the two aggregates stay decoupled.
"""

from __future__ import annotations

from equipment_borrowing.domain.borrowings.value_objects import BorrowingId
from equipment_borrowing.domain.equipment.errors import EquipmentNotAvailable
from equipment_borrowing.domain.equipment.value_objects import EquipmentId, EquipmentStatus


class Equipment:
    """Guard the availability of one physical item."""

    def __init__(
        self,
        equipment_id: EquipmentId,
        category: str,
        status: EquipmentStatus = EquipmentStatus.AVAILABLE,
    ) -> None:
        self._equipment_id = equipment_id
        self._category = category
        self._status = status
        self._checked_out_to: BorrowingId | None = None

    @property
    def equipment_id(self) -> EquipmentId:
        """Return this entity's stable identity."""

        return self._equipment_id

    @property
    def category(self) -> str:
        return self._category

    @property
    def status(self) -> EquipmentStatus:
        return self._status

    @property
    def checked_out_to(self) -> BorrowingId | None:
        """Return the borrowing holding this item, if any."""

        return self._checked_out_to

    @property
    def is_available(self) -> bool:
        return self._status is EquipmentStatus.AVAILABLE

    def ensure_can_check_out(self) -> None:
        """Raise ``EquipmentNotAvailable`` unless this item is Available."""

        if not self.is_available:
            raise EquipmentNotAvailable(self._equipment_id, self._status)

    def check_out(self, borrowing_id: BorrowingId) -> None:
        """Mark this item as taken by a borrowing, following BR5's request from Aggregate A.

        Equipment does not trust the caller (or the event) blindly: it raises
        ``EquipmentNotAvailable`` when the item is checked out or under repair,
        leaving its state unchanged.
        """

        self.ensure_can_check_out()
        self._status = EquipmentStatus.CHECKED_OUT
        self._checked_out_to = borrowing_id

    def send_to_repair(self) -> None:
        """Take an Available item out of circulation for repair."""

        self.ensure_can_check_out()
        self._status = EquipmentStatus.UNDER_REPAIR
