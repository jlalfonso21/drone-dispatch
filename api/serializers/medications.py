from rest_framework import serializers

from misc.models import Medication


class MedicationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ("name", "weight", "code", "image",)


class MedicationLoadSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    qty = serializers.IntegerField(default=0)
