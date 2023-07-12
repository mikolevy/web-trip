from datetime import time

import pytest

from trip_assistance.bus_ride import BusStopOnRide, BusRide
from trip_assistance.models import BusLine
from trip_assistance.trip_recommender import TripProposal


@pytest.fixture
def first_stop_on_ride() -> BusStopOnRide:
    return BusStopOnRide(
        identifier=1,
        name="Stop-1",
        latitude=10.25,
        longitude=20.55,
        order=1,
        time=time(hour=10, minute=55),
    )


@pytest.fixture
def second_stop_on_ride() -> BusStopOnRide:
    return BusStopOnRide(
        identifier=2,
        name="Stop-2",
        latitude=10.35,
        longitude=20.65,
        order=2,
        time=time(hour=11, minute=5),
    )


@pytest.fixture
def third_stop_on_ride() -> BusStopOnRide:
    return BusStopOnRide(
        identifier=3,
        name="Stop-3",
        latitude=10.45,
        longitude=20.75,
        order=3,
        time=time(hour=11, minute=17),
    )

@pytest.fixture
def bus_stop_not_on_ride() -> BusStopOnRide:
    return BusStopOnRide(
        identifier=4,
        name="Stop-4",
        latitude=14.25,
        longitude=24.55,
        order=1,
        time=time(hour=17, minute=20),
    )


@pytest.fixture
def trip_proposal(
    first_stop_on_ride: BusStopOnRide,
    second_stop_on_ride: BusStopOnRide,
    third_stop_on_ride: BusStopOnRide,
) -> TripProposal:
    return TripProposal(
        line_number="N5",
        stops_on_trip=[first_stop_on_ride, second_stop_on_ride, third_stop_on_ride],
    )


@pytest.fixture
def bus_ride(
    first_stop_on_ride: BusStopOnRide,
    second_stop_on_ride: BusStopOnRide,
    third_stop_on_ride: BusStopOnRide,
) -> BusRide:
    return BusRide(
        line_number="1", stops=[first_stop_on_ride, second_stop_on_ride, third_stop_on_ride]
    )

@pytest.fixture
def bus_lines(db) -> list[BusLine]:
    return [
        BusLine.objects.create(number="TestLine-1"),
        BusLine.objects.create(number="TestLine-2"),
    ]