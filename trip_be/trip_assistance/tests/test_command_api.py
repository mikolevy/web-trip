# from datetime import datetime
# from http import HTTPStatus
#
# import pytest
# import pytz
# from django.test import Client
# from django.urls import reverse
# from freezegun import freeze_time
#
# # @pytest.mark.django_db
# @freeze_time("2023-07-09 10:21:35")
# def test_existing_trip_proposal(client: Client) -> None:
#     url = reverse("propose-trip")
#
#     response = client.post(
#         url,
#         data={
#             "src_address": "Startowa 2D",
#             "dst_address": "Aleja Zwycięstwa 15",
#             "bus_number": "8",
#         },
#         headers={"accept": "application/json"},
#     )
#
#     assert response.status_code == HTTPStatus.OK
#     assert response.data == {
#         "arrivalTime": "12:39",
#         "departureTime": "12:26",
#         "dstLocation": (54.37536, 18.6266),
#         "dstStop": "Politechnika SKM",
#         "srcLocation": (54.3967, 18.59796),
#         "srcStop": "Startowa",
#         "stops": [
#             (54.3967, 18.59796),
#             (54.39431, 18.60203),
#             (54.39185, 18.6061),
#             (54.38974, 18.6084),
#             (54.38697, 18.61073),
#             (54.3835, 18.61455),
#             (54.3829, 18.62181),
#             (54.3789, 18.62246),
#             (54.37641, 18.62351),
#             (54.37536, 18.6266),
#         ],
#     }
#
#
# # @pytest.mark.django_db
# @freeze_time("2023-07-09 10:21:35")
# def test_returns_not_found_when_trip_proposal_not_exists(client: Client) -> None:
#     url = reverse("propose-trip")
#
#     response = client.post(
#         url,
#         data={
#             "src_address": "Startowa 2D",
#             "dst_address": "Aleja Zwycięstwa 15",
#             "bus_number": "3",
#         },
#         headers={"accept": "application/json"},
#     )
#
#     assert response.status_code == HTTPStatus.NOT_FOUND
