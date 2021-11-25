from rest_framework import serializers

from misc.models import Drone


class DroneBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ("serial_number", "model", "weight_limit", "battery_capacity", "state",)


class DroneCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ("serial_number", "model", "weight_limit", "battery_capacity",)
