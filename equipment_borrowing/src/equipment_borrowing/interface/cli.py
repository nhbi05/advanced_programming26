"""The minimal entry point: a demo scenario run against the wired application.

Wiring lives in interface/composition.py and sample data in
infrastructure/sample_data.py. This module only turns input into request
DTOs and response DTOs into output -- it never touches a domain object, and
no business rule is implemented here.
"""

from __future__ import annotations

from equipment_borrowing.application.borrowings.dtos import (
    ApproveBorrowingRequest,
    ApproveBorrowingResponse,
)
from equipment_borrowing.infrastructure.sample_data import load_sample_data
from equipment_borrowing.interface.composition import build_application


def show(response: ApproveBorrowingResponse) -> str:
    status = response.status or "-"
    return f"{response.borrowing_id}: {response.outcome.value} (status: {status})"


def main() -> None:
    app = build_application()
    load_sample_data(app.borrowing_repository, app.equipment_repository)

    for borrowing_id in ("B-001", "B-001", "B-002", "B-999"):
        response = app.approve_borrowing.handle(ApproveBorrowingRequest(borrowing_id))
        print(show(response))


if __name__ == "__main__":
    main()
