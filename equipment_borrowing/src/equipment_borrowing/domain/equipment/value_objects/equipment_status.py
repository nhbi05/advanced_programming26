"""The states an Equipment item can be in. See the Equipment aggregate root."""

from enum import Enum


class EquipmentStatus(Enum):
    """Restrict an Equipment item to Available, Checked out or Under repair.

    Only an Available item may be checked out (BR5).
    """

    AVAILABLE = "Available"
    CHECKED_OUT = "Checked out"
    UNDER_REPAIR = "Under repair"
