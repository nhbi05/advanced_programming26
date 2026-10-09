from equipment_borrowing.domain.equipment.equipment import Equipment
from equipment_borrowing.domain.equipment.value_objects import EquipmentId
from equipment_borrowing.infrastructure.equipment.in_memory_equipment_repository import (
    InMemoryEquipmentRepository,
)


def test_a_saved_equipment_item_can_be_fetched_by_its_id() -> None:
    repository = InMemoryEquipmentRepository()
    projector = Equipment(EquipmentId("PRJ-01"), "Projector")

    repository.save(projector)

    assert repository.get(EquipmentId("PRJ-01")) is projector


def test_a_missing_equipment_item_returns_none() -> None:
    assert InMemoryEquipmentRepository().get(EquipmentId("PRJ-99")) is None
