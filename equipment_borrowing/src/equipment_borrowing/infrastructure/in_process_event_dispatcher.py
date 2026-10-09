"""A deliberately small, synchronous, in-process EventDispatcher implementation.

This is not a message broker -- it is a plain registry of Python callables,
invoked directly on the same thread as the Application Service that raised
the event. That is all the brief asks for: "simple in-process handling."
A handler's exception propagates back to that service.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Callable

from equipment_borrowing.application.event_dispatcher import EventDispatcher


class InProcessEventDispatcher(EventDispatcher):
    """Route a domain event to every handler registered for its type."""

    def __init__(self) -> None:
        self._handlers: dict[type, list[Callable[[object], None]]] = defaultdict(list)

    def register(self, event_type: type, handler: Callable[[object], None]) -> None:
        self._handlers[event_type].append(handler)

    def dispatch(self, event: object) -> None:
        for handler in self._handlers[type(event)]:
            handler(event)
