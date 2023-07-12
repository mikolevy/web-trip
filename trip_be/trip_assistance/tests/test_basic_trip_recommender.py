from datetime import datetime

import pytest
import pytz
from freezegun import freeze_time

from trip_assistance.bus_ride import BusStop, BusRide
from trip_assistance.tests.providers import MockyGeoProvider, MockyBusRepo
from trip_assistance.trip_recommender import BasicTripRecommender, TripParams

RECOMMENDATION_DATETIME = datetime(2020, 3, 21, 10, 21, 35)
RECOMMENDATION_DATETIME_STR = RECOMMENDATION_DATETIME.strftime("%Y-%m-%d")


@pytest.fixture
def bus_repo_for_ride(bus_ride: BusRide) -> MockyBusRepo:

    bus_stops_by_date = {RECOMMENDATION_DATETIME_STR: bus_ride.stops}
    bus_rides_by_line_and_date = {(bus_ride.line_number, RECOMMENDATION_DATETIME_STR): [bus_ride]}
    return MockyBusRepo(
        bus_stops_by_date=bus_stops_by_date, bus_rides_by_line_and_date=bus_rides_by_line_and_date
    )


@pytest.fixture
def trip_params_for_ride(bus_ride: BusRide) -> TripParams:
    return TripParams(src_address="1.75", dst_address="1.55", bus_number=bus_ride.line_number)


@freeze_time("2020-03-21 10:21:35")
def test_init_default_with_current_datetime() -> None:
    trip_recommender = BasicTripRecommender()
    expected_datetime = datetime(2020, 3, 21, 10, 21, 35).astimezone(
        pytz.timezone("Europe/Warsaw")
    )

    assert trip_recommender.walking_distance_in_m == 400
    assert trip_recommender.recommendation_datetime == expected_datetime


def test_returns_only_bus_stops_in_walking_range() -> None:
    geo_provider = MockyGeoProvider()
    recommendation_datetime = datetime(2020, 3, 21, 10, 21, 35)
    recommendation_datetime_str = "2020-03-21"
    trip_recommender = BasicTripRecommender(recommendation_datetime=recommendation_datetime)

    reference_point = (2, 50)
    stops_in_walking_distance = [
        BusStop(identifier=1, name="Test-1", latitude=2, longitude=50),
        BusStop(identifier=2, name="Test-2", latitude=4, longitude=50),
    ]
    stops_not_in_walking_distance = [
        BusStop(identifier=3, name="Test-3", latitude=3, longitude=50),
        BusStop(identifier=4, name="Test-4", latitude=11, longitude=50),
    ]
    bus_stops_by_date = {
        recommendation_datetime_str: stops_in_walking_distance + stops_not_in_walking_distance
    }
    bus_repo = MockyBusRepo(bus_stops_by_date=bus_stops_by_date)

    result = trip_recommender.bus_stops_in_walking_range(reference_point, bus_repo, geo_provider)

    assert result == stops_in_walking_distance


def test_recommends_correct_ride(
    bus_ride: BusRide, bus_repo_for_ride: MockyBusRepo, trip_params_for_ride: TripParams
) -> None:
    geo_provider = MockyGeoProvider()
    trip_recommender = BasicTripRecommender(recommendation_datetime=RECOMMENDATION_DATETIME)

    result = trip_recommender.recommend_trip(trip_params_for_ride, bus_repo_for_ride, geo_provider)

    assert result.line_number == bus_ride.line_number
    assert result.stops_on_trip == bus_ride.stops


def test_not_recommend_past_rides(
    bus_ride: BusRide, bus_repo_for_ride: MockyBusRepo, trip_params_for_ride: TripParams
) -> None:
    geo_provider = MockyGeoProvider()
    recommendation_datetime = datetime(2020, 3, 21, 23, 21, 35)
    trip_recommender = BasicTripRecommender(recommendation_datetime=recommendation_datetime)

    result = trip_recommender.recommend_trip(trip_params_for_ride, bus_repo_for_ride, geo_provider)

    assert result is None


def test_not_recommend_other_date_rides(
    bus_ride: BusRide, bus_repo_for_ride: MockyBusRepo, trip_params_for_ride: TripParams
) -> None:
    geo_provider = MockyGeoProvider()
    trip_recommender = BasicTripRecommender(recommendation_datetime=RECOMMENDATION_DATETIME)

    bus_rides_by_line_and_date = {(bus_ride.line_number, "2020-03-22"): [bus_ride]}
    bus_repo_for_ride.bus_rides_by_line_and_date = bus_rides_by_line_and_date

    result = trip_recommender.recommend_trip(trip_params_for_ride, bus_repo_for_ride, geo_provider)

    assert result is None


def test_not_recommend_other_line_rides(
    bus_ride: BusRide, bus_repo_for_ride: MockyBusRepo, trip_params_for_ride: TripParams
) -> None:
    geo_provider = MockyGeoProvider()
    trip_recommender = BasicTripRecommender(recommendation_datetime=RECOMMENDATION_DATETIME)

    bus_rides_by_line_and_date = {("Other-line", RECOMMENDATION_DATETIME_STR): [bus_ride]}
    bus_repo_for_ride.bus_rides_by_line_and_date = bus_rides_by_line_and_date

    result = trip_recommender.recommend_trip(trip_params_for_ride, bus_repo_for_ride, geo_provider)

    assert result is None


def test_not_recommend_rides_without_selected_src_stop(
    bus_ride: BusRide, bus_repo_for_ride: MockyBusRepo, trip_params_for_ride: TripParams
) -> None:
    geo_provider = MockyGeoProvider()
    trip_recommender = BasicTripRecommender(recommendation_datetime=RECOMMENDATION_DATETIME)
    del bus_ride.stops[0]

    result = trip_recommender.recommend_trip(trip_params_for_ride, bus_repo_for_ride, geo_provider)

    assert result is None


def test_not_recommend_rides_without_selected_dst_stop(
    bus_ride: BusRide, bus_repo_for_ride: MockyBusRepo, trip_params_for_ride: TripParams
) -> None:
    geo_provider = MockyGeoProvider()
    trip_recommender = BasicTripRecommender(recommendation_datetime=RECOMMENDATION_DATETIME)
    del bus_ride.stops[2]

    result = trip_recommender.recommend_trip(trip_params_for_ride, bus_repo_for_ride, geo_provider)

    assert result is None
