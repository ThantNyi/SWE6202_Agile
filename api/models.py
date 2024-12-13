from django.db import models

# Create your models here.
class EnergyData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    energy_output_mw = models.FloatField()

class CarbonOffset(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    offset_tons = models.FloatField()

class OperationalMetric(models.Model):
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)