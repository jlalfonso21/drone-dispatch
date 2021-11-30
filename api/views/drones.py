import json

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from api.errors import MedicationNotFoundError, WeightError, BatteryLevelError
from api.serializers.drones import DroneBaseSerializer, DroneCreateSerializer, DroneSerialNumberSerializer, \
    DroneCargoSerializer, CargoItemSerializer, HistoricalRecordField
from api.serializers.medications import MedicationLoadSerializer
from misc.models import Drone, Medication


class DroneCreate(CreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneCreateSerializer


class DroneAvailableList(ListAPIView):
    queryset = Drone.objects.filter(state="IDLE")
    serializer_class = DroneBaseSerializer


class DronesViewSet(viewsets.ModelViewSet):
    queryset = Drone.objects.all()
    serializer_class = DroneSerialNumberSerializer

    @action(detail=False, methods=['get'])
    def loaded_meds(self, request, serial_number=None):
        obj: Drone = self.queryset.filter(serial_number=serial_number).first()
        if obj is None:
            return Response(data={"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)
        cargo = obj.get_or_create_cargo()
        data = CargoItemSerializer(cargo.items.all(), many=True).data
        return Response(data=data)

    @action(detail=False, methods=['get'])
    def battery_level(self, request, serial_number=None):
        obj: Drone = self.queryset.filter(serial_number=serial_number).first()
        if obj is None:
            return Response(data={"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=obj.battery_capacity)

    @action(detail=False, methods=['post'])
    def load_drone(self, request, serial_number=None):
        obj: Drone = self.queryset.filter(serial_number=serial_number).first()
        if obj is None:
            return Response(data={"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        objs = None
        if isinstance(data, str):
            data = json.loads(data)
        if isinstance(data, list):
            objs = MedicationLoadSerializer(data=data, many=True)
        elif isinstance(data, dict):
            objs = MedicationLoadSerializer(data=data)
        else:
            pass

        try:
            objs.is_valid()
            data = objs.validated_data
            if isinstance(data, dict):
                data = [data, ]
        except:
            return Response({"detail": "parsing error"}, status=status.HTTP_400_BAD_REQUEST)

        meds_to_add = []
        try:
            for i in data:
                med = Medication.objects.filter(code=i['code']).first()
                if med is None:
                    raise MedicationNotFoundError()
                else:
                    meds_to_add.append((med, i['qty'],))
        except:
            return Response(data={"detail": "medication not found"}, status=status.HTTP_400_BAD_REQUEST)

        cargo = obj.get_or_create_cargo()
        if not cargo.can_load_this_weight_list([i[0].weight * i[1] for i in meds_to_add]):
            return Response(data={"weight_exceed": "the cargo weight exceeds drone weight limit"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            for item in meds_to_add:
                obj.add_med(item[0], item[1])
        except WeightError:
            return Response(data={"weight_exceed": "the cargo weight exceeds drone weight limit"},
                            status=status.HTTP_400_BAD_REQUEST)
        except BatteryLevelError:
            return Response(data={"battery_low": "the drone cannot be in loading state since its battery level is low"},
                            status=status.HTTP_400_BAD_REQUEST)
        data = DroneCargoSerializer(obj).data
        return Response(data=data)

    @action(detail=False, methods=['post'])
    def clean_cargo(self, request, serial_number=None):
        obj: Drone = self.queryset.filter(serial_number=serial_number).first()
        if obj is None:
            return Response(data={"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)
        obj.clean_cargo()
        return Response()

    @action(detail=False, methods=['get'])
    def audit(self, request, serial_number=None):
        obj: Drone = self.queryset.filter(serial_number=serial_number).first()
        if obj is None:
            return Response(data={"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)
        srz = HistoricalRecordField()
        data = srz.to_representation(data=obj.history.all())

        # remove unnecesary data
        for d in data:
            del d['id']
            del d['history_id']
            del d['history_change_reason']
            del d['history_type']
        return Response(data=data)
