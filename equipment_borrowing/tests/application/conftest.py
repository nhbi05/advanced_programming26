"""Provide a full, in-memory Application for use-case-level tests -- built by
the same composition root the CLI uses, so tests exercise the real wiring
rather than a copy of it.
"""

from __future__ import annotations

from datetime import date

import pytest

from equipment_borrowing.domain.borrowings.borrowing import Borrowing
from equipment_borrowing.domain.borrowings.value_objects import BorrowingId, BorrowPeriod
from equipment_borrowing.domain.equipment.equipment import Equipment
from equipment_borrowing.domain.equipment.value_objects import EquipmentId, EquipmentStatus
from equipment_borrowing.interface.composition import Application, build_application

PERIOD = BorrowPeriod(date(2026, 10, 12), date(2026, 10, 15))


@pytest.fixture
def app() -> Application:
    application = build_application()
    application.equipment_repository.save(Equipment(EquipmentId("PRJ-01"), "Projector"))
    application.equipment_repository.save(Equipment(EquipmentId("HDMI-01"), "HDMI cable"))
    application.equipment_repository.save(
        Equipment(EquipmentId("PRJ-02"), "Projector", EquipmentStatus.UNDER_REPAIR)
    )
    return application


@pytest.fixture
def save_borrowing(app):
    """Save a Requested borrowing of the given equipment ids."""

    def save(borrowing_id: str, *equipment_ids: str) -> None:
        app.borrowing_repository.save(
            Borrowing(
                BorrowingId(borrowing_id),
                PERIOD,
                [EquipmentId(value) for value in equipment_ids],
            )
        )

    return save
