from rest_framework import serializers
from .models import EnergyData, CarbonOffset, OperationalMetric

class BulkListSerializer(serializers.ListSerializer):
    """Custom ListSerializer for handling bulk operations."""

    def create(self, validated_data):
        instances = [self.child.create(attrs) for attrs in validated_data]
        return self.child.Meta.model.objects.bulk_create(instances)

class EnergyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyData
        fields = '__all__'
        list_serializer_class = BulkListSerializer

class CarbonOffsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarbonOffset
        fields = '__all__'
        list_serializer_class = BulkListSerializer

class OperationalMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationalMetric
        fields = '__all__'
        list_serializer_class = BulkListSerializer
