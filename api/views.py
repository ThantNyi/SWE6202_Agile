from django.shortcuts import render


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

class EnergyDataView(APIView):
    def get(self, request):
        energy_data = EnergyData.objects.all()
        serializer = EnergyDataSerializer(energy_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EnergyDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
