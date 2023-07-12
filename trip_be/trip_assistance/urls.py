from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from trip_assistance import crud_api, command_api

urlpatterns = [
    path("bus-lines", crud_api.bus_lines, name="bus-lines"),
    path("propose-trip", command_api.propose_trip, name="propose-trip"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
