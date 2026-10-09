from datetime import date

import pytest

from equipment_borrowing.domain.borrowings.borrowing import Borrowing
from equipment_borrowing.domain.borrowings.services import LateReturnPolicy
from equipment_borrowing.domain.borrowings.value_objects import BorrowingId, BorrowPeriod
from equipment_borrowing.domain.equipment.equipment import Equipment
from equipment_borrowing.domain.equipment.errors import UnknownEquipmentCategory
from equipment_borrowing.domain.equipment.value_objects import EquipmentId

END = date(2026, 10, 3)
BORROWING = Borrowing(
    BorrowingId("B-001"), BorrowPeriod(date(2026, 10, 1), END), [EquipmentId("X-01")]
)
policy = LateReturnPolicy()


def item(category: str) -> Equipment:
    return Equipment(EquipmentId("X-01"), category)


def test_br4_a_projector_three_days_late_earns_six_suspension_days() -> None:
    # The worked example from the slides: 3 x 2 = 6.
    assert policy.suspension_days(BORROWING, item("Projector"), date(2026, 10, 6)) == 6


def test_br4_an_hdmi_cable_two_days_late_earns_two_suspension_days() -> None:
    assert policy.suspension_days(BORROWING, item("HDMI cable"), date(2026, 10, 5)) == 2


def test_br4_markers_one_day_late_earn_one_suspension_day() -> None:
    assert policy.suspension_days(BORROWING, item("Markers"), date(2026, 10, 4)) == 1


def test_br4_an_on_time_return_earns_no_suspension() -> None:
    assert policy.suspension_days(BORROWING, item("Projector"), END) == 0


def test_br4_an_unknown_category_is_rejected() -> None:
    with pytest.raises(UnknownEquipmentCategory) as exception_info:
        policy.suspension_days(BORROWING, item("Laptop"), date(2026, 10, 6))

    assert exception_info.value.category == "Laptop"


def test_br4_category_lookup_ignores_case_and_surrounding_spaces() -> None:
    assert policy.weight_for("  PROJECTOR ") == 2
