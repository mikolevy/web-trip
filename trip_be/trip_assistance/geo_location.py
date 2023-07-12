from typing import Protocol

from geopy import Nominatim
from geopy.distance import distance, Distance


GeoLocation = tuple[float, float]


class GeoProvider(Protocol):
    @staticmethod
    def distance(a_location: GeoLocation, b_location: GeoLocation) -> Distance:
        ...

    @staticmethod
    def address_to_location(address: str) -> GeoLocation:
        ...


class GeopyProvider:
    @staticmethod
    def distance(a_location: GeoLocation, b_location: GeoLocation) -> Distance:
        return distance(a_location, b_location)

    @staticmethod
    def address_to_location(address: str) -> GeoLocation:
        geolocator = Nominatim(user_agent="webinar-agent")
        address_code = geolocator.geocode(address)
        return address_code.latitude, address_code.longitude
