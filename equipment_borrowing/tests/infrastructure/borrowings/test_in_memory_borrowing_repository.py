from datetime import date

from equipment_borrowing.domain.borrowings.borrowing import Borrowing
from equipment_borrowing.domain.borrowings.value_objects import BorrowingId, BorrowPeriod
from equipment_borrowing.domain.equipment.value_objects import EquipmentId
from equipment_borrowing.infrastructure.borrowings.in_memory_borrowing_repository import (
    InMemoryBorrowingRepository,
)


def test_a_saved_borrowing_can_be_fetched_by_its_id() -> None:
    repository = InMemoryBorrowingRepository()
    borrowing = Borrowing(
        BorrowingId("B-001"),
        BorrowPeriod(date(2026, 10, 1), date(2026, 10, 3)),
        [EquipmentId("PRJ-01")],
    )

    repository.save(borrowing)

    assert repository.get(BorrowingId("B-001")) is borrowing


def test_br6_a_missing_borrowing_returns_none() -> None:
    assert InMemoryBorrowingRepository().get(BorrowingId("B-999")) is None
