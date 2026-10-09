"""The EquipmentRepository contract, the abstraction used to fetch Aggregate B.

Defined in Application because its only user is the
CheckOutEquipmentOnApproval handler; Infrastructure implements it
(infrastructure/equipment/in_memory_equipment_repository.py).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from equipment_borrowing.domain.equipment.equipment import Equipment
from equipment_borrowing.domain.equipment.value_objects import EquipmentId


class EquipmentRepository(ABC):
    """Persist and retrieve Equipment aggregates by their identity."""

    @abstractmethod
    def save(self, equipment: Equipment) -> None:
        """Store an equipment item, replacing any previous version of it."""

    @abstractmethod
    def get(self, equipment_id: EquipmentId) -> Equipment | None:
        """Return the equipment with this id, or None when it does not exist."""
