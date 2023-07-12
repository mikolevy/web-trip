from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from trip_assistance.models import BusLine
from trip_assistance.serializers import BusLineSerializer


@api_view(["GET"])
def bus_lines(request: Request) -> Response:
    all_bus_lines = BusLine.objects.all().order_by("number")
    serializer = BusLineSerializer(all_bus_lines, many=True)
    return Response(serializer.data)


