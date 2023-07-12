from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from trip_assistance.models import BusLine


@pytest.mark.django_db
def test_getting_all_bus_lines(client: Client, bus_lines: list[BusLine]) -> None:
    url = reverse("bus-lines")

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert len(response.data) == len(bus_lines)
    assert response.data[0]["number"] == bus_lines[0].number
    assert response.data[1]["number"] == bus_lines[1].number

