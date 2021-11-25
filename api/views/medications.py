from rest_framework.generics import ListCreateAPIView

from api.serializers.medications import MedicationBaseSerializer
from misc.models import Medication


class MedicationListCreate(ListCreateAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationBaseSerializer
