from django.shortcuts import render
from django.db import transaction

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EnergyData, CarbonOffset, OperationalMetric
from .serializers import EnergyDataSerializer, CarbonOffsetSerializer, OperationalMetricSerializer

# Create your views here.
def home(request):
    return render(request, 'index.html')

def data_visualization(request):
    return render(request, 'data.html') # Renders the 'data.html' template

class BulkUpdateMixin:
    def bulk_update(self, model, serializer_class, data_list):
        """Perform bulk updates for the given model."""
        instances = []
        updatable_fields = ['energy_output_mw']  # Explicitly define updatable fields

        for item in data_list:
            instance = model.objects.get(id=item['id'])  # Match by id
            for attr, value in item.items():
                if attr in updatable_fields:  # Only update allowed fields
                    setattr(instance, attr, value)
            instances.append(instance)

        # Perform bulk update
        model.objects.bulk_update(instances, updatable_fields)

class EnergyDataView(APIView):
    def get(self, request):
        energy_data = EnergyData.objects.all()
        serializer = EnergyDataSerializer(energy_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Handle bulk creation of energy data."""
        if isinstance(request.data, list):  # Check for bulk data
            serializer = EnergyDataSerializer(data=request.data, many=True)
        else:  # Handle single record
            serializer = EnergyDataSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EnergyDataUpdateView(APIView, BulkUpdateMixin):
    def put(self, request):
        """Handle bulk update of energy data."""
        try:
            with transaction.atomic():
                self.bulk_update(EnergyData, EnergyDataSerializer, request.data)
            return Response({"message": "Bulk update successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class EnergyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyData
        fields = ['id', 'timestamp', 'energy_output_mw']  # Include only valid fields
        
class EnergyDataDeleteView(APIView):
    def delete(self, request):
        """Handle bulk deletion of energy data."""
        ids = request.data.get("ids", [])
        if not ids:
            return Response({"error": "No ids provided"}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count, _ = EnergyData.objects.filter(id__in=ids).delete()
        return Response({"message": f"Deleted {deleted_count} records"}, status=status.HTTP_200_OK)

class CarbonOffsetView(APIView):
    def get(self, request):
        carbon_offsets = CarbonOffset.objects.all()
        serializer = CarbonOffsetSerializer(carbon_offsets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarbonOffsetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OperationalMetricView(APIView):
    def get(self, request):
        operational_metrics = OperationalMetric.objects.all()
        serializer = OperationalMetricSerializer(operational_metrics, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OperationalMetricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
