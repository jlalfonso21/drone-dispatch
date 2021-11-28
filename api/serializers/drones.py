from rest_framework import serializers

from misc.models import Drone, Cargo, CargoItem


class CargoItemSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_code(self, obj: CargoItem):
        return obj.med.code

    def get_name(self, obj: CargoItem):
        return obj.med.name

    class Meta:
        model = CargoItem
        fields = ("code", "name", "qty")


class CargoSerializer(serializers.ModelSerializer):
    items = CargoItemSerializer(many=True)

    class Meta:
        model = Cargo
        fields = ("items",)


class DroneBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ("serial_number", "model", "weight_limit", "battery_capacity", "state",)


class DroneCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ("serial_number", "model", "weight_limit", "battery_capacity",)


class DroneCargoSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    loaded_weight = serializers.SerializerMethodField()

    def get_items(self, obj: Drone):
        cargo = obj.get_or_create_cargo()
        return CargoItemSerializer(cargo.items.all(), many=True).data

    def get_loaded_weight(self, obj: Drone):
        cargo = obj.get_or_create_cargo()
        return cargo.get_total_weight()

    class Meta:
        model = Drone
        fields = ("serial_number", "weight_limit", "loaded_weight", "battery_capacity", "items")


class DroneSerialNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ("serial_number",)
