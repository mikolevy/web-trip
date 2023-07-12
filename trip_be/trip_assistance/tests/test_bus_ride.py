from datetime import time

import pytest

from trip_assistance.bus_ride import BusRide, BusStopOnRide


def test_getting_stop_by_id(bus_ride: BusRide, second_stop_on_ride: BusStopOnRide) -> None:
    bus_stop = bus_ride.stop_by_id(second_stop_on_ride.identifier)

    assert bus_stop is second_stop_on_ride


def test_stop_by_id_returns_none_when_no_matching_stop(bus_ride: BusRide) -> None:
    bus_stop = bus_ride.stop_by_id(-200)

    assert bus_stop is None


def test_stops_on_ride_returns_only_from_available_stops(
    bus_ride: BusRide,
    first_stop_on_ride: BusStopOnRide,
    second_stop_on_ride: BusStopOnRide,
    bus_stop_not_on_ride: BusStopOnRide,
) -> None:
    available_stops = [bus_stop_not_on_ride, first_stop_on_ride, second_stop_on_ride]
    expected_result = [first_stop_on_ride, second_stop_on_ride]
    stops_on_ride = bus_ride.stops_on_ride(available_stops)

    assert stops_on_ride == expected_result


def test_stops_on_ride_when_no_stops_available(bus_ride: BusRide) -> None:
    stops_on_ride = bus_ride.stops_on_ride([])

    assert stops_on_ride == []


def test_stops_on_ride_when_no_stops_matching(
    bus_ride: BusRide, bus_stop_not_on_ride: BusStopOnRide
) -> None:
    stops_on_ride = bus_ride.stops_on_ride([bus_stop_not_on_ride])

    assert stops_on_ride == []


def test_stops_between(
    bus_ride: BusRide, second_stop_on_ride: BusStopOnRide, third_stop_on_ride: BusStopOnRide
) -> None:
    stops_between = bus_ride.stops_between(second_stop_on_ride, third_stop_on_ride)

    assert stops_between == [second_stop_on_ride, third_stop_on_ride]


# def test_stops_between_raises_when_stop_does_not_exist() -> None:
#     pass
