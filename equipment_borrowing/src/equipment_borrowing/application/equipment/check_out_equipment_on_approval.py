"""CheckOutEquipmentOnApproval: the handler side of BR5.

This is deliberately in Application, not Domain: it needs a repository to
fetch Equipment, which is a coordination concern. Whether an item may be
checked out is still decided entirely by Equipment itself.
"""

from __future__ import annotations

from equipment_borrowing.application.equipment.equipment_repository import EquipmentRepository
from equipment_borrowing.domain.borrowings.events import BorrowingApproved
from equipment_borrowing.domain.equipment.equipment import Equipment
from equipment_borrowing.domain.equipment.errors import EquipmentNotFound
from equipment_borrowing.domain.equipment.value_objects import EquipmentId


class CheckOutEquipmentOnApproval:
    """Check out every item of a newly approved borrowing, or none of them."""

    # The event this handler reacts to, so the composition root can register
    # it without importing anything from the domain.
    event_type = BorrowingApproved

    def __init__(self, equipment_repository: EquipmentRepository) -> None:
        self._equipment_repository = equipment_repository

    def __call__(self, event: BorrowingApproved) -> None:
        items = [self._load(equipment_id) for equipment_id in event.equipment_ids]

        # Ask every item first, so one unavailable item never leaves the
        # others half checked out.
        for item in items:
            item.ensure_can_check_out()

        for item in items:
            item.check_out(event.borrowing_id)
            self._equipment_repository.save(item)

    def _load(self, equipment_id: EquipmentId) -> Equipment:
        item = self._equipment_repository.get(equipment_id)
        if item is None:
            raise EquipmentNotFound(equipment_id)
        return item
