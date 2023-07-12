import dataclasses
import json
import math
import os
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Protocol, TypedDict

import requests

from trip_assistance.bus_ride import BusStop, BusStopOnRide, BusRide
from trip_be.settings import BASE_DIR


class StopTimesDict(TypedDict):
    stopSequence: int
    stopId: int
    departureTime: str


class SchedulesData(TypedDict):
    stopTimes: list[StopTimesDict]


@dataclass
class Vehicle:
    line_number: str
    latitude: float
    longitude: float

    @property
    def location(self):
        return self.latitude, self.longitude


class BusRepo(Protocol):
    def get_all_vehicles(self) -> list[Vehicle]:
        ...

    def get_all_bus_stops(self, date_obj: date) -> list[BusStop]:
        ...

    def get_bus_rides_for_line(self, line_number: str, date_obj: date) -> list[BusRide]:
        ...


class FileRemoteBusRepo:
    DEPARTURE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
    SCHEDULES_DATE_FORMAT = "%Y-%m-%d"

    def __init__(
        self,
        vehicles_data_url: str = "https://ckan2.multimediagdansk.pl/gpsPositions",
        bus_data_dir: str = "bus_data",
        bus_stops_filename: str = "bus_stops.json",
        bus_schedules_dir: str = "schedules",
    ) -> None:
        self.vehicles_data_url = vehicles_data_url
        self.bus_data_dir = bus_data_dir
        self.bus_stops_filename = bus_stops_filename
        self.bus_schedules_dir = bus_schedules_dir
        self.bus_stops_file_path = os.path.join(
            BASE_DIR, self.bus_data_dir, self.bus_stops_filename
        )

    def get_all_vehicles(self) -> list[Vehicle]:
        vehicles_response = requests.get(self.vehicles_data_url)
        vehicles_data = vehicles_response.json()

        return [
            Vehicle(
                line_number=vehicle_info["Line"],
                latitude=vehicle_info["Lat"],
                longitude=vehicle_info["Lon"],
            )
            for vehicle_info in vehicles_data["Vehicles"]
        ]

    def get_all_bus_stops(self, date_obj: date) -> list[BusStop]:
        with open(self.bus_stops_file_path) as bus_stops_file:
            bus_stops_by_date = json.load(bus_stops_file)

        date_str = date_obj.strftime(FileRemoteBusRepo.SCHEDULES_DATE_FORMAT)
        bus_stops_data = bus_stops_by_date[date_str]["stops"]
        return [
            BusStop(
                identifier=bus_info["stopId"],
                name=bus_info["stopDesc"],
                latitude=bus_info["stopLat"],
                longitude=bus_info["stopLon"],
            )
            for bus_info in bus_stops_data
        ]

    def get_bus_rides_for_line(self, line_number: str, date_obj: date) -> list[BusRide]:
        all_bus_stops = self.get_all_bus_stops(date_obj)
        bus_stop_by_id = {bus_stop.identifier: bus_stop for bus_stop in all_bus_stops}
        path_to_schedules = self._schedules_file_path(line_number, date_obj)
        with open(path_to_schedules) as schedules_file:
            schedules_data = json.load(schedules_file)

        return self.bus_rides_from_schedules_data(schedules_data, bus_stop_by_id, line_number)

    def bus_rides_from_schedules_data(
        self, schedules_data: SchedulesData, bus_stop_by_id: dict[int, BusStop], line_number: str
    ) -> list[BusRide]:
        bus_rides: list[BusRide] = []
        previous_stop_order = math.inf
        for stop_info in schedules_data["stopTimes"]:

            stop_order = stop_info["stopSequence"]
            if stop_order < previous_stop_order:
                ride = BusRide(line_number=line_number, stops=[])
                bus_rides.append(ride)

            stop_id = stop_info["stopId"]
            base_bus_data = bus_stop_by_id[stop_id]
            departure_time = self._stop_info_departure_time_to_time(stop_info["departureTime"])
            bus_stop_on_ride = BusStopOnRide(
                **dataclasses.asdict(base_bus_data),
                order=stop_order,
                time=departure_time,
            )
            ride.stops.append(bus_stop_on_ride)

            previous_stop_order = stop_order

        return bus_rides

    def _schedules_file_path(self, line_number: str, date_obj: date) -> str:
        file_name = f"{line_number}.json"
        date_str = date_obj.strftime(FileRemoteBusRepo.SCHEDULES_DATE_FORMAT)
        return os.path.join(
            BASE_DIR, self.bus_data_dir, self.bus_schedules_dir, date_str, file_name
        )

    @staticmethod
    def _stop_info_departure_time_to_time(departure_time: str) -> time:
        return datetime.strptime(departure_time, FileRemoteBusRepo.DEPARTURE_TIME_FORMAT).time()
