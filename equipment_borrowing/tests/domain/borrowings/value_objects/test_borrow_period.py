from dataclasses import FrozenInstanceError
from datetime import date

import pytest

from equipment_borrowing.domain.borrowings.errors import InvalidBorrowPeriod
from equipment_borrowing.domain.borrowings.value_objects import BorrowPeriod


def test_br1_a_one_day_period_is_valid() -> None:
    period = BorrowPeriod(date(2026, 10, 1), date(2026, 10, 2))

    assert period.length_in_days == 1


def test_br1_a_fourteen_day_period_is_valid() -> None:
    # Boundary case: exactly the maximum.
    period = BorrowPeriod(date(2026, 10, 1), date(2026, 10, 15))

    assert period.length_in_days == 14


def test_br1_a_fifteen_day_period_is_rejected() -> None:
    with pytest.raises(InvalidBorrowPeriod) as exception_info:
        BorrowPeriod(date(2026, 10, 1), date(2026, 10, 16))

    assert "at most 14 days" in str(exception_info.value)


def test_br1_an_end_on_the_same_day_as_the_start_is_rejected() -> None:
    with pytest.raises(InvalidBorrowPeriod):
        BorrowPeriod(date(2026, 10, 1), date(2026, 10, 1))


def test_br1_an_end_before_the_start_is_rejected() -> None:
    with pytest.raises(InvalidBorrowPeriod) as exception_info:
        BorrowPeriod(date(2026, 10, 5), date(2026, 10, 1))

    assert "must fall after" in str(exception_info.value)


def test_br1_periods_with_the_same_dates_are_equal() -> None:
    assert BorrowPeriod(date(2026, 10, 1), date(2026, 10, 3)) == BorrowPeriod(
        date(2026, 10, 1), date(2026, 10, 3)
    )


def test_br1_a_period_is_immutable() -> None:
    period = BorrowPeriod(date(2026, 10, 1), date(2026, 10, 3))

    with pytest.raises(FrozenInstanceError):
        period.end = date(2026, 12, 31)  # type: ignore[misc]


def test_days_late_is_zero_on_or_before_the_end_date() -> None:
    period = BorrowPeriod(date(2026, 10, 1), date(2026, 10, 3))

    assert period.days_late(date(2026, 10, 2)) == 0
    assert period.days_late(date(2026, 10, 3)) == 0


def test_days_late_counts_days_after_the_end_date() -> None:
    period = BorrowPeriod(date(2026, 10, 1), date(2026, 10, 3))

    assert period.days_late(date(2026, 10, 6)) == 3
