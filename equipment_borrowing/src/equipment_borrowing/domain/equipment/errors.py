"""Rule violations raised by the Equipment aggregate and its collaborators."""

from __future__ import annotations

from typing import TYPE_CHECKING

from equipment_borrowing.domain.errors import DomainError

if TYPE_CHECKING:
    from equipment_borrowing.domain.equipment.value_objects import EquipmentId, EquipmentStatus


class EquipmentNotAvailable(DomainError):
    """BR5: equipment can only be checked out while it is Available."""

    def __init__(self, equipment_id: EquipmentId, current_status: EquipmentStatus) -> None:
        self.equipment_id = equipment_id
        self.current_status = current_status
        super().__init__(
            f"Equipment {equipment_id} is {current_status.value} and cannot be checked out."
        )


class EquipmentNotFound(DomainError):
    """BR5: an approved borrowing refers to equipment that does not exist."""

    def __init__(self, equipment_id: EquipmentId) -> None:
        self.equipment_id = equipment_id
        super().__init__(f"Equipment {equipment_id} was not found.")


class UnknownEquipmentCategory(DomainError):
    """BR4: the late return policy has no weight for this category."""

    def __init__(self, category: str) -> None:
        self.category = category
        super().__init__(f'No suspension weight is defined for category "{category}".')
