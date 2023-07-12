from trip_assistance.serializers import TripProposalSerializer
from trip_assistance.trip_recommender import TripProposal


def test_trip_proposal_to_response(trip_proposal: TripProposal) -> None:
    serializer = TripProposalSerializer()

    serialized_response = serializer.to_response(trip_proposal)

    assert serialized_response["departureTime"] == "10:55"
    assert serialized_response["arrivalTime"] == "11:17"
    assert serialized_response["srcStop"] == "Stop-1"
    assert serialized_response["dstStop"] == "Stop-3"
    assert serialized_response["srcLocation"] == (10.25, 20.55)
    assert serialized_response["dstLocation"] == (10.45, 20.75)
    assert len(serialized_response["stops"]) == 3
    assert serialized_response["stops"][0] == (10.25, 20.55)
    assert serialized_response["stops"][1] == (10.35, 20.65)
    assert serialized_response["stops"][2] == (10.45, 20.75)
