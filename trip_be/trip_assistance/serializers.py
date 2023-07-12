from typing import Any, TypedDict, Literal

from rest_framework import serializers

# from trip_assistance.geo_location import GeoLocation
from trip_assistance.models import BusLine
# from trip_assistance.trip_recommender import TripProposal


class BusLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusLine
        fields = ["id", "number"]


# class TripProposalData(TypedDict):
#     departureTime: str
#     arrivalTime: str
#     srcStop: str
#     dstStop: str
#     srcLocation: GeoLocation
#     dstLocation: GeoLocation
#     stops: list[GeoLocation]
#
# class TripProposalSerializer:
#     TIME_FORMAT = "%H:%M"
#
#     def to_response(self, trip_proposal: TripProposal) -> TripProposalData:
#         return {
#             "departureTime": trip_proposal.departure.strftime(self.TIME_FORMAT),
#             "arrivalTime": trip_proposal.arrival.strftime(self.TIME_FORMAT),
#             "srcStop": trip_proposal.src_stop.name,
#             "dstStop": trip_proposal.dst_stop.name,
#             "srcLocation": trip_proposal.src_stop.location,
#             "dstLocation": trip_proposal.dst_stop.location,
#             "stops": [stop.location for stop in trip_proposal.stops_on_trip]
#         }
