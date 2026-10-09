"""Sample equipment and borrowings preloaded into the in-memory repositories.

With no database, the demo needs some existing data to approve. Preloading
storage is a persistence concern, so it lives in Infrastructure; the
Interface layer can then run the demo through Application DTOs alone,
without ever constructing a domain object itself.
"""

from __future__ import annotations

from datetime import date

from equipment_borrowing.application.borrowings.borrowing_repository import BorrowingRepository
from equipment_borrowing.application.equipment.equipment_repository import EquipmentRepository
from equipment_borrowing.domain.borrowings.borrowing import Borrowing
from equipment_borrowing.domain.borrowings.value_objects import BorrowingId, BorrowPeriod
from equipment_borrowing.domain.equipment.equipment import Equipment
from equipment_borrowing.domain.equipment.value_objects import EquipmentId, EquipmentStatus


def load_sample_data(
    borrowing_repository: BorrowingRepository,
    equipment_repository: EquipmentRepository,
) -> None:
    """Store three items and two Requested borrowings.

    B-001 asks for two Available items; B-002 asks for a projector that is
    Under repair, so approving it shows BR5's check-out being refused.
    """

    equipment_repository.save(Equipment(EquipmentId("PRJ-01"), "Projector"))
    equipment_repository.save(Equipment(EquipmentId("HDMI-01"), "HDMI cable"))
    equipment_repository.save(
        Equipment(EquipmentId("PRJ-02"), "Projector", EquipmentStatus.UNDER_REPAIR)
    )

    period = BorrowPeriod(date(2026, 10, 12), date(2026, 10, 15))
    borrowing_repository.save(
        Borrowing(BorrowingId("B-001"), period, [EquipmentId("PRJ-01"), EquipmentId("HDMI-01")])
    )
    borrowing_repository.save(Borrowing(BorrowingId("B-002"), period, [EquipmentId("PRJ-02")]))
