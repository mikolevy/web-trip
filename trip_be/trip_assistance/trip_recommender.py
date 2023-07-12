import datetime
from dataclasses import dataclass
from typing import List, Optional, Protocol

import pytz

from trip_assistance.bus_repo import BusRepo
from trip_assistance.bus_ride import BusStopOnRide, BusStop
from trip_assistance.geo_location import GeoProvider, GeoLocation


@dataclass
class TripParams:
    src_address: str
    dst_address: str
    bus_number: str


@dataclass
class TripProposal:
    line_number: str
    stops_on_trip: List[BusStopOnRide]

    @property
    def src_stop(self) -> BusStopOnRide:
        return self.stops_on_trip[0]

    @property
    def dst_stop(self) -> BusStopOnRide:
        return self.stops_on_trip[-1]

    @property
    def departure(self) -> datetime.time:
        return self.src_stop.time

    @property
    def arrival(self) -> datetime.time:
        return self.dst_stop.time


class TripRecommender(Protocol):
    def bus_stops_in_walking_range(
        self, reference_point: GeoLocation, bus_repo: BusRepo, geo_provider: GeoProvider
    ) -> list[BusStop]:
        ...

    def recommend_trip(
        self,
        trip_params: TripParams,
        bus_repo: BusRepo,
        geo_provider: GeoProvider,
    ) -> Optional[TripProposal]:
        ...


class BasicTripRecommender:
    def __init__(self, walking_distance_in_m: int = 400, recommendation_datetime=None) -> None:
        self.walking_distance_in_m = walking_distance_in_m
        if recommendation_datetime is None:
            recommendation_datetime = datetime.datetime.now()
            recommendation_datetime = recommendation_datetime.astimezone(pytz.timezone("Europe/Warsaw"))
        self.recommendation_datetime = recommendation_datetime

    def bus_stops_in_walking_range(
        self, reference_point: GeoLocation, bus_repo: BusRepo, geo_provider: GeoProvider
    ) -> list[BusStop]:
        all_bus_stops = bus_repo.get_all_bus_stops(self.recommendation_datetime.date())
        return [
            bus_stop
            for bus_stop in all_bus_stops
            if geo_provider.distance(reference_point, bus_stop.location).meters
            <= self.walking_distance_in_m
        ]

    def recommend_trip(
        self,
        trip_params: TripParams,
        bus_repo: BusRepo,
        geo_provider: GeoProvider,
    ) -> Optional[TripProposal]:
        bus_rides_of_line = bus_repo.get_bus_rides_for_line(
            trip_params.bus_number, self.recommendation_datetime.date()
        )
        proposals_of_future_rides: List[TripProposal] = []
        src_location = geo_provider.address_to_location(trip_params.src_address)
        dst_location = geo_provider.address_to_location(trip_params.dst_address)
        available_src_stops = self.bus_stops_in_walking_range(src_location, bus_repo, geo_provider)
        available_dst_stops = self.bus_stops_in_walking_range(dst_location, bus_repo, geo_provider)
        for ride in bus_rides_of_line:

            src_stops_on_ride = ride.stops_on_ride(available_src_stops)
            dst_stops_on_ride = ride.stops_on_ride(available_dst_stops)

            for src_stop in src_stops_on_ride:
                for dst_stop in dst_stops_on_ride:
                    if src_stop.order > dst_stop.order:
                        continue

                    stops_on_trip = ride.stops_between(src_stop, dst_stop)
                    trip_proposal = TripProposal(
                        line_number=ride.line_number, stops_on_trip=stops_on_trip
                    )

                    if trip_proposal.departure > self.recommendation_datetime.time():
                        proposals_of_future_rides.append(trip_proposal)

        if proposals_of_future_rides:
            proposals_of_future_rides.sort(key=lambda proposal: proposal.departure)
            return proposals_of_future_rides[0]
        return None
