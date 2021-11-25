from rest_framework.generics import ListAPIView, CreateAPIView

from api.serializers.drones import DroneBaseSerializer, DroneCreateSerializer
from misc.models import Drone


class DroneCreate(CreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneCreateSerializer


class DroneAvailableList(ListAPIView):
    queryset = Drone.objects.filter(state="IDLE")
    serializer_class = DroneBaseSerializer
