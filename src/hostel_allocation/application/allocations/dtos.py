"""Input and output DTOs for the two Allocation use cases.

DTOs cross the Application Service boundary as plain data -- callers never
pass or receive domain objects (Allocation, Room, value objects) directly.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AllocateRoomRequest:
    allocation_number: str
    student_id: str
    room_number: str
    academic_year: str


@dataclass(frozen=True, slots=True)
class AllocateRoomResponse:
    success: bool
    message: str
    allocation_number: str | None = None


@dataclass(frozen=True, slots=True)
class CancelAllocationRequest:
    allocation_number: str


@dataclass(frozen=True, slots=True)
class CancelAllocationResponse:
    success: bool
    message: str
