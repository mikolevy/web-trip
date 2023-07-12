import pytest

from trip_assistance.models import BusLine


@pytest.fixture
def bus_lines(db) -> list[BusLine]:
    return [
        BusLine.objects.create(number="TestLine-1"),
        BusLine.objects.create(number="TestLine-2"),
    ]
