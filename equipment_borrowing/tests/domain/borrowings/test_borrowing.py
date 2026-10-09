from datetime import date

import pytest

from equipment_borrowing.domain.borrowings.borrowing import Borrowing
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

PERIOD = BorrowPeriod(date(2026, 10, 1), date(2026, 10, 3))


def new_borrowing(*equipment_ids: str) -> Borrowing:
    return Borrowing(
        BorrowingId("B-001"),
        PERIOD,
        [EquipmentId(value) for value in equipment_ids or ("PRJ-01",)],
    )


# BR2: Requested -> Approved -> Returned


def test_br2_a_new_borrowing_starts_requested() -> None:
    assert new_borrowing().status is BorrowingStatus.REQUESTED


def test_br2_a_requested_borrowing_can_be_approved() -> None:
    borrowing = new_borrowing()

    borrowing.approve()

    assert borrowing.status is BorrowingStatus.APPROVED


def test_br2_a_borrowing_cannot_be_approved_twice() -> None:
    borrowing = new_borrowing()
    borrowing.approve()
    borrowing.pull_pending_events()

    with pytest.raises(InvalidBorrowState) as exception_info:
        borrowing.approve()

    assert "while it is Approved" in str(exception_info.value)
    assert borrowing.status is BorrowingStatus.APPROVED
    assert borrowing.pull_pending_events() == []


def test_br2_an_approved_borrowing_can_be_returned() -> None:
    borrowing = new_borrowing()
    borrowing.approve()

    borrowing.mark_returned()

    assert borrowing.status is BorrowingStatus.RETURNED


def test_br2_a_requested_borrowing_cannot_be_returned() -> None:
    borrowing = new_borrowing()

    with pytest.raises(InvalidBorrowState):
        borrowing.mark_returned()

    assert borrowing.status is BorrowingStatus.REQUESTED


def test_br2_a_returned_borrowing_cannot_be_approved_again() -> None:
    borrowing = new_borrowing()
    borrowing.approve()
    borrowing.mark_returned()

    with pytest.raises(InvalidBorrowState):
        borrowing.approve()


def test_br2_items_cannot_be_added_after_approval() -> None:
    borrowing = new_borrowing("PRJ-01")
    borrowing.approve()

    with pytest.raises(InvalidBorrowState):
        borrowing.add_equipment(EquipmentId("HDMI-01"))


# BR3: 1-3 distinct items


def test_br3_a_borrowing_can_hold_three_items() -> None:
    # Boundary case: exactly the maximum.
    borrowing = new_borrowing("PRJ-01", "HDMI-01", "MRK-01")

    assert len(borrowing.equipment_ids) == 3


def test_br3_an_empty_borrowing_is_rejected() -> None:
    with pytest.raises(InvalidBorrowingContents):
        Borrowing(BorrowingId("B-001"), PERIOD, [])


def test_br3_four_items_are_rejected() -> None:
    with pytest.raises(InvalidBorrowingContents):
        new_borrowing("PRJ-01", "HDMI-01", "MRK-01", "MRK-02")


def test_br3_a_duplicate_item_is_rejected() -> None:
    with pytest.raises(InvalidBorrowingContents) as exception_info:
        new_borrowing("PRJ-01", "PRJ-01")

    assert "twice" in str(exception_info.value)


def test_br3_adding_a_fourth_item_is_rejected_and_contents_are_unchanged() -> None:
    borrowing = new_borrowing("PRJ-01", "HDMI-01", "MRK-01")

    with pytest.raises(InvalidBorrowingContents):
        borrowing.add_equipment(EquipmentId("MRK-02"))

    assert len(borrowing.equipment_ids) == 3


def test_br3_adding_an_item_already_held_is_rejected() -> None:
    borrowing = new_borrowing("PRJ-01")

    with pytest.raises(InvalidBorrowingContents):
        borrowing.add_equipment(EquipmentId("PRJ-01"))


# BR5: approval raises BorrowingApproved


def test_br5_approving_raises_a_borrowing_approved_event() -> None:
    borrowing = new_borrowing("PRJ-01", "HDMI-01")

    borrowing.approve()
    events = borrowing.pull_pending_events()

    assert len(events) == 1
    assert isinstance(events[0], BorrowingApproved)
    assert events[0].borrowing_id == BorrowingId("B-001")
    assert events[0].equipment_ids == (EquipmentId("PRJ-01"), EquipmentId("HDMI-01"))
    assert borrowing.pull_pending_events() == []
