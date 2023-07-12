# from http import HTTPStatus

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

# from trip_assistance.bus_repo import FileRemoteBusRepo
# from trip_assistance.geo_location import GeopyProvider
# from trip_assistance.serializers import TripProposalSerializer
# from trip_assistance.trip_recommender import BasicTripRecommender, TripParams


@api_view(["POST"])
def propose_trip(request: Request) -> Response:
    pass
    # trip_params = TripParams(
    #     src_address=request.data["src_address"],
    #     dst_address=request.data["dst_address"],
    #     bus_number=request.data["bus_number"],
    # )
    # trip_recommender = BasicTripRecommender()
    # trip_proposal = trip_recommender.recommend_trip(
    #     trip_params, FileRemoteBusRepo(), GeopyProvider()
    # )
    # if trip_proposal:
    #     serializer = TripProposalSerializer()
    #     return Response(serializer.to_response(trip_proposal))
    # return Response(status=HTTPStatus.NOT_FOUND)
