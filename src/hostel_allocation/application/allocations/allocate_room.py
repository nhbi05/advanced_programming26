"""AllocateRoomService: the first of the two connected use cases.

This Application Service coordinates BR1, BR3 and BR4 -- it does not
implement any of them itself. Every rule check happens inside the domain
objects/services it calls; this class only sequences the calls and
translates the result into a DTO.
"""

from __future__ import annotations

from hostel_allocation.application.allocations.dtos import (
    AllocateRoomRequest,
    AllocateRoomResponse,
)
from hostel_allocation.application.error_messages import describe
from hostel_allocation.domain.allocations.allocation import Allocation
from hostel_allocation.domain.allocations.repositories import AllocationRepository
from hostel_allocation.domain.allocations.services import AllocationEligibilityService
from hostel_allocation.domain.allocations.value_objects import AcademicYear, AllocationNumber, StudentId
from hostel_allocation.domain.errors import DomainError
from hostel_allocation.domain.rooms.repositories import RoomRepository
from hostel_allocation.domain.rooms.value_objects import RoomNumber


class AllocateRoomService:
    """Allocate a room to a student, given repository implementations from outside."""

    def __init__(
        self,
        allocation_repository: AllocationRepository,
        room_repository: RoomRepository,
        eligibility_service: AllocationEligibilityService,
    ) -> None:
        self._allocation_repository = allocation_repository
        self._room_repository = room_repository
        self._eligibility_service = eligibility_service

    def handle(self, request: AllocateRoomRequest) -> AllocateRoomResponse:
        try:
            room = self._room_repository.get(RoomNumber(request.room_number))
            student_id = StudentId(request.student_id)

            self._eligibility_service.check(student_id, room)  # BR4

            allocation = Allocation(
                allocation_number=AllocationNumber(request.allocation_number),
                student_id=student_id,
                room_number=room.room_number,
                academic_year=AcademicYear.parse(request.academic_year),  # BR1
            )
            room.add_occupant(allocation.allocation_number)  # BR3

            self._allocation_repository.save(allocation)
            self._room_repository.save(room)
        except DomainError as error:
            return AllocateRoomResponse(success=False, message=describe(error))

        return AllocateRoomResponse(
            success=True,
            message="Allocation created.",
            allocation_number=str(allocation.allocation_number),
        )
