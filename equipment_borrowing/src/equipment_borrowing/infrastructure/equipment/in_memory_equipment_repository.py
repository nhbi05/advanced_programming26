"""The in-memory EquipmentRepository implementation used for this coursework."""

from __future__ import annotations

from equipment_borrowing.application.equipment.equipment_repository import EquipmentRepository
from equipment_borrowing.domain.equipment.equipment import Equipment
from equipment_borrowing.domain.equipment.value_objects import EquipmentId


class InMemoryEquipmentRepository(EquipmentRepository):
    def __init__(self) -> None:
        self._equipment: dict[EquipmentId, Equipment] = {}

    def save(self, equipment: Equipment) -> None:
        self._equipment[equipment.equipment_id] = equipment

    def get(self, equipment_id: EquipmentId) -> Equipment | None:
        return self._equipment.get(equipment_id)
