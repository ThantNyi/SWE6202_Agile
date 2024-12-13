from rest_framework import serializers
from .models import EnergyData, CarbonOffset, OperationalMetric

class EnergyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyData
        fields = '__all__'

class CarbonOffsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarbonOffset
        fields = '__all__'

class OperationalMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationalMetric
        fields = '__all__'
