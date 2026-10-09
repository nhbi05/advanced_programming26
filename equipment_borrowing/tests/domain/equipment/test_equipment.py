import pytest

from equipment_borrowing.domain.borrowings.value_objects import BorrowingId
from equipment_borrowing.domain.equipment.equipment import Equipment
from equipment_borrowing.domain.equipment.errors import EquipmentNotAvailable
from equipment_borrowing.domain.equipment.value_objects import EquipmentId, EquipmentStatus


def new_projector(status: EquipmentStatus = EquipmentStatus.AVAILABLE) -> Equipment:
    return Equipment(EquipmentId("PRJ-01"), "Projector", status)


def test_available_equipment_can_be_checked_out() -> None:
    projector = new_projector()

    projector.check_out(BorrowingId("B-001"))

    assert projector.status is EquipmentStatus.CHECKED_OUT
    assert projector.checked_out_to == BorrowingId("B-001")


def test_br5_equipment_under_repair_cannot_be_checked_out() -> None:
    projector = new_projector(EquipmentStatus.UNDER_REPAIR)

    with pytest.raises(EquipmentNotAvailable) as exception_info:
        projector.check_out(BorrowingId("B-001"))

    assert "Under repair" in str(exception_info.value)
    assert projector.status is EquipmentStatus.UNDER_REPAIR
    assert projector.checked_out_to is None


def test_br5_equipment_already_checked_out_cannot_be_checked_out_again() -> None:
    projector = new_projector()
    projector.check_out(BorrowingId("B-001"))

    with pytest.raises(EquipmentNotAvailable):
        projector.check_out(BorrowingId("B-002"))

    assert projector.checked_out_to == BorrowingId("B-001")


def test_available_equipment_can_be_sent_to_repair() -> None:
    projector = new_projector()

    projector.send_to_repair()

    assert projector.status is EquipmentStatus.UNDER_REPAIR
