import pytest

from hostel_allocation.domain.rooms.value_objects import Capacity


def test_capacity_accepts_a_value_within_the_allowed_range() -> None:
    capacity = Capacity(4)

    assert int(capacity) == 4


def test_capacity_rejects_zero() -> None:
    with pytest.raises(ValueError):
        Capacity(0)


def test_capacity_rejects_a_value_above_the_maximum() -> None:
    with pytest.raises(ValueError):
        Capacity(9)
