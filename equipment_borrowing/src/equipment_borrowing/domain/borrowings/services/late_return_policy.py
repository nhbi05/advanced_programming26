"""LateReturnPolicy. See BR4 (cross-concept rule).

Suspension days = days late x category weight. A Domain Service because
the days late come from the Borrowing and the weight comes from the
Equipment's category, so the rule fits neither entity.

Stateless: it only calculates; it does not apply the suspension.
"""

from __future__ import annotations

from datetime import date

from equipment_borrowing.domain.borrowings.borrowing import Borrowing
from equipment_borrowing.domain.equipment.equipment import Equipment
from equipment_borrowing.domain.equipment.errors import UnknownEquipmentCategory

CATEGORY_WEIGHTS: dict[str, int] = {
    "projector": 2,
    "hdmi cable": 1,
    "markers": 1,
}


class LateReturnPolicy:
    """Calculate the suspension a late return earns."""

    def suspension_days(
        self, borrowing: Borrowing, equipment: Equipment, returned_on: date
    ) -> int:
        """Return days late x category weight (0 when returned on time).

        Raises ``UnknownEquipmentCategory`` for a category with no weight,
        even when the item is returned on time.
        """

        weight = self.weight_for(equipment.category)
        return borrowing.days_late(returned_on) * weight

    def weight_for(self, category: str) -> int:
        try:
            return CATEGORY_WEIGHTS[category.strip().lower()]
        except KeyError:
            raise UnknownEquipmentCategory(category) from None
