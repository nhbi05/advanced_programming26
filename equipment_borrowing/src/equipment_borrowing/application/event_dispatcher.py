"""The EventDispatcher contract used to publish domain events (BR5).

Abstractions are defined in the layer that uses them: ApproveBorrowingService
needs to publish BorrowingApproved, so this contract lives in Application.
How events are delivered is a technical detail, implemented in
infrastructure/in_process_event_dispatcher.py.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class EventDispatcher(ABC):
    """Deliver a domain event to every handler interested in it."""

    @abstractmethod
    def dispatch(self, event: object) -> None:
        """Run the handlers for this event; a handler's exception propagates."""
