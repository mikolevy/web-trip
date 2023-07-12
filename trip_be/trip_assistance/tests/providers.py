from datetime import date
from typing import Optional

from geopy.distance import Distance

from trip_assistance.bus_repo import Vehicle
from trip_assistance.bus_ride import BusStop, BusRide
from trip_assistance.geo_location import GeoLocation


class MockyGeoProvider:

    @staticmethod
    def distance(a_location: GeoLocation, b_location: GeoLocation) -> Distance:
        if (a_location[0] + b_location[0]) % 2 == 0:
            return Distance(0.1)
        return Distance(2)

    @staticmethod
    def address_to_location(address: str) -> GeoLocation:
        return float(address), float(address)


BusStopsByDateDict = dict[str, list[BusStop]]
BusRidesByLineAndDateDict = dict[tuple[str, str], list[BusRide]]


class MockyBusRepo:
    SCHEDULES_DATE_FORMAT = "%Y-%m-%d"

    def __init__(
        self,
        all_vehicles: Optional[list[Vehicle]] = None,
        bus_stops_by_date: Optional[BusStopsByDateDict] = None,
        bus_rides_by_line_and_date: Optional[BusRidesByLineAndDateDict] = None,
    ):
        if not all_vehicles:
            all_vehicles = []
        if not bus_stops_by_date:
            bus_stops_by_date = {}
        if not bus_rides_by_line_and_date:
            bus_rides_by_line_and_date = {}
        self.all_vehicles = all_vehicles
        self.bus_stops_by_date = bus_stops_by_date
        self.bus_rides_by_line_and_date = bus_rides_by_line_and_date

    def get_all_vehicles(self) -> list[Vehicle]:
        return self.all_vehicles

    def get_all_bus_stops(self, date_obj: date) -> list[BusStop]:
        date_str = date_obj.strftime(self.SCHEDULES_DATE_FORMAT)
        return self.bus_stops_by_date.get(date_str, [])

    def get_bus_rides_for_line(self, line_number: str, date_obj: date) -> list[BusRide]:
        date_str = date_obj.strftime(self.SCHEDULES_DATE_FORMAT)
        return self.bus_rides_by_line_and_date.get((line_number, date_str), [])
