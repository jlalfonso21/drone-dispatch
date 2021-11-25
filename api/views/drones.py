from rest_framework.generics import CreateAPIView

from api.serializers.drones import DroneCreateSerializer
from misc.models import Drone


class DroneCreate(CreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneCreateSerializer
