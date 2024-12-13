from django.urls import path
from .views import home, data_visualization, EnergyDataView, CarbonOffsetView, OperationalMetricView

urlpatterns = [
    path('', home, name='home'),
    path('data/', data_visualization, name='data'),
    path('energy-data/', EnergyDataView.as_view(), name='energy-data'),
    path('carbon-offsets/', CarbonOffsetView.as_view(), name='carbon-offsets'),
    path('operational-metrics/', OperationalMetricView.as_view(), name='operational-metrics'),
]
