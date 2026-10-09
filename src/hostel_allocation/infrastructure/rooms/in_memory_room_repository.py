"""The in-memory RoomRepository implementation used for this coursework."""

from __future__ import annotations

from hostel_allocation.domain.rooms.errors import RoomNotFound
from hostel_allocation.domain.rooms.repositories import RoomRepository
from hostel_allocation.domain.rooms.room import Room
from hostel_allocation.domain.rooms.value_objects import RoomNumber


class InMemoryRoomRepository(RoomRepository):
    def __init__(self) -> None:
        self._rooms: dict[RoomNumber, Room] = {}

    def save(self, room: Room) -> None:
        self._rooms[room.room_number] = room

    def get(self, room_number: RoomNumber) -> Room:
        try:
            return self._rooms[room_number]
        except KeyError as error:
            raise RoomNotFound(room_number) from error
