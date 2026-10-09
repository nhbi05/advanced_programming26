"""The EquipmentId value object that identifies one physical item."""

from __future__ import annotations

from dataclasses import dataclass

from equipment_borrowing.domain.errors import BlankIdentifier


@dataclass(frozen=True, slots=True)
class EquipmentId:
    """An item's asset tag, e.g. PRJ-01."""

    value: str

    def __post_init__(self) -> None:
        """Protect the rule that an equipment id must carry real text."""

        if not self.value.strip():
            raise BlankIdentifier("equipment id")

    def __str__(self) -> str:
        return self.value
