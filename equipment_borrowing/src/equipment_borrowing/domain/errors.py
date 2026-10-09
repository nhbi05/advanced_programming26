"""The base of every rule violation the domain can report.

Each subclass carries the facts of the violation as attributes (which
borrowing, which equipment) so callers can react to *what* happened without
parsing text. Domain objects throw these; the application service converts
them into outcomes.

DomainError extends ValueError so code that only needs "this input broke a
rule" can keep catching ValueError.
"""

from __future__ import annotations


class DomainError(ValueError):
    """A business rule refused an operation."""


class BlankIdentifier(DomainError):
    """An identifier value object was given empty or whitespace-only text."""

    def __init__(self, identifier_name: str) -> None:
        self.identifier_name = identifier_name
        super().__init__(f"A {identifier_name} cannot be blank.")
