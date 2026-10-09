"""The RoomRepository contract, the abstraction used to fetch Aggregate B."""

from __future__ import annotations

from abc import ABC, abstractmethod

from hostel_allocation.domain.rooms.room import Room
from hostel_allocation.domain.rooms.value_objects import RoomNumber


class RoomRepository(ABC):
    """Persist and retrieve Room aggregates by their identity."""

    @abstractmethod
    def save(self, room: Room) -> None:
        """Store a room, replacing any previous version of it."""

    @abstractmethod
    def get(self, room_number: RoomNumber) -> Room:
        """Return the room with this number.

        Raises ``RoomNotFound`` when no such room exists.
        """
