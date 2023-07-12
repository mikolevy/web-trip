from rest_framework import serializers

from trip_assistance.models import BusLine


class BusLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusLine
        fields = ["id", "number"]
