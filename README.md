# Hostel Allocation

A Python project organized using Clean Architecture and Domain-Driven Design.
Housing staff allocate students to hostel rooms and cancel those allocations.

## Layers

- `domain`: aggregates, entities, value objects, domain services, domain events and repository contracts
- `application`: use cases (application services), DTOs and domain event handlers
- `infrastructure`: in-memory repository implementations
- `interface`: the minimal command-line entry point

Dependencies point inward: interface and infrastructure depend on application/domain, while domain depends on no framework.

## Aggregates

- `Allocation` (Aggregate A), in `domain/allocations`: BR2 Active -> Cancelled, raises `AllocationCancelled` (BR5)
- `Room` (Aggregate B), in `domain/rooms`: BR3 occupants never exceed capacity

## Business rules

| Rule | Responsible component |
| ---- | --------------------- |
| BR1 | `AcademicYear` value object |
| BR2 | `Allocation.cancel()` |
| BR3 | `Room.add_occupant()` |
| BR4 | `AllocationEligibilityService` |
| BR5 | `AllocationCancelled` -> `ReleaseRoomOnAllocationCancelled` -> `Room.release_occupant()` |
| BR6 | `AllocationRepository.get()` used by `CancelAllocationService` |

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m hostel_allocation.interface.cli
```

## Test

```powershell
pytest
```

28 tests pass (`docs/tdd_evidence/full_suite_final_run.txt`). Test identifiers T1-T8 and BR1-BR6 appear in the test function names across `tests/`.

## TDD evidence

BR3 (Room capacity) was built test-first. `Room.add_occupant()` was written without its capacity guard, producing a failing run (`docs/tdd_evidence/br3_1_failing_red.txt`); the guard was then added, producing a passing run (`docs/tdd_evidence/br3_2_passing_green.txt`).

## AI use

Claude Code (Anthropic) helped scaffold the project structure and code, and ran the TDD red/green cycle for BR3, matching the course demo project's style.
