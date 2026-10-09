"""The composition root: the one place concrete implementations are chosen.

This module only builds and connects objects -- it seeds no data and runs no
scenario. Like the rest of Interface, it imports nothing from Domain: it
picks Infrastructure implementations and hands them to Application. Swapping the in-memory repositories for real ones, or registering
another event handler, changes this file and nothing else. Every entry point
(the CLI, the tests) gets a fully wired application from build_application().
"""

from __future__ import annotations

from dataclasses import dataclass

from equipment_borrowing.application.borrowings.approve_borrowing import ApproveBorrowingService
from equipment_borrowing.application.borrowings.borrowing_repository import BorrowingRepository
from equipment_borrowing.application.equipment.check_out_equipment_on_approval import (
    CheckOutEquipmentOnApproval,
)
from equipment_borrowing.application.equipment.equipment_repository import EquipmentRepository
from equipment_borrowing.infrastructure.borrowings.in_memory_borrowing_repository import (
    InMemoryBorrowingRepository,
)
from equipment_borrowing.infrastructure.equipment.in_memory_equipment_repository import (
    InMemoryEquipmentRepository,
)
from equipment_borrowing.infrastructure.in_process_event_dispatcher import (
    InProcessEventDispatcher,
)


@dataclass(frozen=True)
class Application:
    """The wired use case, plus the repositories behind it."""

    borrowing_repository: BorrowingRepository
    equipment_repository: EquipmentRepository
    approve_borrowing: ApproveBorrowingService


def build_application() -> Application:
    borrowing_repository = InMemoryBorrowingRepository()
    equipment_repository = InMemoryEquipmentRepository()

    check_out_equipment = CheckOutEquipmentOnApproval(equipment_repository)
    event_dispatcher = InProcessEventDispatcher()
    event_dispatcher.register(check_out_equipment.event_type, check_out_equipment)

    return Application(
        borrowing_repository=borrowing_repository,
        equipment_repository=equipment_repository,
        approve_borrowing=ApproveBorrowingService(borrowing_repository, event_dispatcher),
    )
