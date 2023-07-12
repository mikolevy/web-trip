from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BusStop:
    identifier: int
    name: str
    latitude: float
    longitude: float

    @property
    def location(self):
        return self.latitude, self.longitude


@dataclass
class BusStopOnRide(BusStop):
    order: int
    time: datetime.time


@dataclass
class BusRide:
    line_number: str
    stops: list[BusStopOnRide]

    def stop_by_id(self, stop_id: int) -> Optional[BusStopOnRide]:
        for stop in self.stops:
            if stop.identifier == stop_id:
                return stop

    def stops_on_ride(self, available_stops: list[BusStop]) -> list[BusStopOnRide]:
        stops_on_ride: list[BusStopOnRide] = []
        for bus_stop in available_stops:
            bus_stop_on_ride = self.stop_by_id(bus_stop.identifier)
            if bus_stop_on_ride:
                stops_on_ride.append(bus_stop_on_ride)
        return stops_on_ride

    def stops_between(self, src_stop: BusStopOnRide, dst_stop: BusStopOnRide) -> list[BusStopOnRide]:
        stops_start_index = self.stops.index(src_stop)
        stops_end_index = self.stops.index(dst_stop) + 1
        return self.stops[stops_start_index:stops_end_index]
