from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from trip_assistance import crud_api

urlpatterns = [
    path("bus-lines", crud_api.bus_lines, name="bus-lines"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
