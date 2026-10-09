# Equipment Borrowing

A Python project organized using Clean Architecture and Domain-Driven Design.
Class representatives borrow equipment (projectors, HDMI cables, markers);
the main use case approves a borrowing and checks out its equipment.

## Layers

- `domain`: aggregates, entities, value objects, domain services and domain events
- `application`: use cases (application services), DTOs, domain event handlers, and the repository and event dispatcher contracts
- `infrastructure`: in-memory repository implementations, the in-process event dispatcher and the demo sample data
- `interface`: the composition root (`composition.py`, wiring only) and the minimal command-line demo (`cli.py`); it talks to Application through DTOs only and never imports Domain

Dependencies point inward: Interface -> Application and Infrastructure; Infrastructure -> Application and Domain; Application -> Domain; Domain depends on nothing. `tests/test_dependency_rule.py` checks this against the real imports.

Abstractions are defined in the layer that uses them. No domain object or domain service uses a repository, so `BorrowingRepository` and `EquipmentRepository` live in Application, next to the services that consume them; Infrastructure implements them. The same goes for `EventDispatcher`, implemented by `InProcessEventDispatcher`.

## Aggregates

- `Borrowing` (Aggregate A), in `domain/borrowings`: BR2 Requested -> Approved -> Returned, BR3 1-3 distinct items, raises `BorrowingApproved` (BR5)
- `Equipment` (Aggregate B), in `domain/equipment`: can be checked out only when Available

## Business rules

| Rule | Responsible component |
| ---- | --------------------- |
| BR1 | `BorrowPeriod` value object |
| BR2 | `Borrowing.approve()` / `Borrowing.mark_returned()` |
| BR3 | `Borrowing` constructor and `Borrowing.add_equipment()` |
| BR4 | `LateReturnPolicy` domain service |
| BR5 | `BorrowingApproved` -> `CheckOutEquipmentOnApproval` -> `Equipment.check_out()` |
| BR6 | `BorrowingRepository.get()` used by `ApproveBorrowingService` |

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m equipment_borrowing.interface.cli
```

## Test

```powershell
pytest
```

Test names start with the rule they cover (`test_br1_...` to `test_br6_...`).
