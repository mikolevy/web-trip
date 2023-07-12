from trip_assistance.bus_ride import BusStopOnRide
from trip_assistance.trip_recommender import TripProposal


def test_src_stop_returns_first_stop(
    trip_proposal: TripProposal, first_stop_on_ride: BusStopOnRide
) -> None:
    assert trip_proposal.src_stop is first_stop_on_ride


def test_dst_stop_returns_last_stop(
    trip_proposal: TripProposal, third_stop_on_ride: BusStopOnRide
) -> None:
    assert trip_proposal.dst_stop is third_stop_on_ride


def test_departure_is_first_stop_time(
    trip_proposal: TripProposal, first_stop_on_ride: BusStopOnRide
) -> None:
    assert trip_proposal.departure == first_stop_on_ride.time


def test_arrival_is_last_stop_time(
    trip_proposal: TripProposal, third_stop_on_ride: BusStopOnRide
) -> None:
    assert trip_proposal.arrival == third_stop_on_ride.time
