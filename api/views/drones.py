from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from api.serializers.drones import DroneBaseSerializer, DroneCreateSerializer
from misc.models import Drone


class DroneCreate(CreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneCreateSerializer


class DroneAvailableList(ListAPIView):
    queryset = Drone.objects.filter(state="IDLE")
    serializer_class = DroneBaseSerializer


class DronesViewSet(viewsets.ModelViewSet):
    queryset = Drone.objects.all()
    serializer_class = DroneBaseSerializer

    @action(detail=False, methods=['get'])
    def battery_level(self, request, serial_number=None):
        obj: Drone = self.queryset.filter(serial_number=serial_number).first()
        if obj is not None:
            return Response(data=obj.battery_capacity)
        else:
            return Response(data={"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)
