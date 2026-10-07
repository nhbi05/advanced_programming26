import pytest

from hostel_allocation.domain.allocations.value_objects import AcademicYear


def test_br1_accepts_two_consecutive_years() -> None:
    academic_year = AcademicYear.parse("2025/2026")

    assert str(academic_year) == "2025/2026"


def test_br1_boundary_accepts_the_smallest_valid_gap() -> None:
    # Boundary case: end year is exactly start year + 1, the smallest valid gap.
    academic_year = AcademicYear.parse("2099/2100")

    assert academic_year.end_year - academic_year.start_year == 1


def test_br1_rejects_years_that_are_not_consecutive() -> None:
    with pytest.raises(ValueError) as exception_info:
        AcademicYear.parse("2025/2027")

    assert "consecutive" in str(exception_info.value)


def test_br1_rejects_the_wrong_separator() -> None:
    with pytest.raises(ValueError):
        AcademicYear.parse("2025-2026")
