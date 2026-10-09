from equipment_borrowing.application.borrowings.dtos import (
    ApprovalOutcome,
    ApproveBorrowingRequest,
)
from equipment_borrowing.domain.borrowings.value_objects import BorrowingId, BorrowingStatus
from equipment_borrowing.domain.equipment.value_objects import EquipmentId, EquipmentStatus


def test_br5_approving_a_borrowing_checks_out_its_equipment_in_aggregate_b(
    app, save_borrowing
) -> None:
    # Successful main use case. Verifies the BorrowingApproved event is
    # handled and Equipment (Aggregate B) changes as expected.
    save_borrowing("B-001", "PRJ-01", "HDMI-01")

    response = app.approve_borrowing.handle(ApproveBorrowingRequest("B-001"))

    assert response.outcome is ApprovalOutcome.APPROVED_AND_CHECKED_OUT
    assert response.borrowing_id == "B-001"
    assert response.status == "Approved"

    borrowing = app.borrowing_repository.get(BorrowingId("B-001"))
    assert borrowing.status is BorrowingStatus.APPROVED

    for equipment_id in ("PRJ-01", "HDMI-01"):
        item = app.equipment_repository.get(EquipmentId(equipment_id))
        assert item.status is EquipmentStatus.CHECKED_OUT
        assert item.checked_out_to == BorrowingId("B-001")


def test_br6_approving_an_unknown_borrowing_returns_not_found(app) -> None:
    response = app.approve_borrowing.handle(ApproveBorrowingRequest("B-999"))

    assert response.outcome is ApprovalOutcome.BORROWING_NOT_FOUND
    assert response.status is None


def test_br2_approving_a_borrowing_twice_returns_invalid_state(app, save_borrowing) -> None:
    save_borrowing("B-001", "PRJ-01")
    app.approve_borrowing.handle(ApproveBorrowingRequest("B-001"))

    response = app.approve_borrowing.handle(ApproveBorrowingRequest("B-001"))

    assert response.outcome is ApprovalOutcome.INVALID_STATE
    assert response.status == "Approved"


def test_br5_equipment_under_repair_gives_approved_but_checkout_failed(
    app, save_borrowing
) -> None:
    # Aggregate B (Equipment) rejects the follow-up action BR5 asks for.
    save_borrowing("B-001", "PRJ-02")

    response = app.approve_borrowing.handle(ApproveBorrowingRequest("B-001"))

    assert response.outcome is ApprovalOutcome.APPROVED_BUT_CHECKOUT_FAILED
    assert response.status == "Approved"
    item = app.equipment_repository.get(EquipmentId("PRJ-02"))
    assert item.status is EquipmentStatus.UNDER_REPAIR


def test_br5_one_unavailable_item_leaves_the_others_available(app, save_borrowing) -> None:
    # All-or-nothing: PRJ-01 must not stay checked out when PRJ-02 fails.
    save_borrowing("B-001", "PRJ-01", "PRJ-02")

    response = app.approve_borrowing.handle(ApproveBorrowingRequest("B-001"))

    assert response.outcome is ApprovalOutcome.APPROVED_BUT_CHECKOUT_FAILED
    item = app.equipment_repository.get(EquipmentId("PRJ-01"))
    assert item.status is EquipmentStatus.AVAILABLE


def test_br5_equipment_taken_by_another_borrowing_cannot_be_checked_out(
    app, save_borrowing
) -> None:
    save_borrowing("B-001", "PRJ-01")
    save_borrowing("B-002", "PRJ-01")
    app.approve_borrowing.handle(ApproveBorrowingRequest("B-001"))

    response = app.approve_borrowing.handle(ApproveBorrowingRequest("B-002"))

    assert response.outcome is ApprovalOutcome.APPROVED_BUT_CHECKOUT_FAILED
    item = app.equipment_repository.get(EquipmentId("PRJ-01"))
    assert item.checked_out_to == BorrowingId("B-001")


def test_br5_missing_equipment_gives_approved_but_checkout_failed(
    app, save_borrowing
) -> None:
    save_borrowing("B-001", "GHOST-01")

    response = app.approve_borrowing.handle(ApproveBorrowingRequest("B-001"))

    assert response.outcome is ApprovalOutcome.APPROVED_BUT_CHECKOUT_FAILED
