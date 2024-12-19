from django.urls import path
from .views import home, data_visualization, EnergyDataView, EnergyDataUpdateView, EnergyDataDeleteView, CarbonOffsetView, OperationalMetricView

urlpatterns = [
    path('', home, name='home'),
    path('data/', data_visualization, name='data'),
    path('energy-data/', EnergyDataView.as_view(), name='energy-data'), # Handles GET and POST (bulk create)
    path('energy-data/bulk-update/', EnergyDataUpdateView.as_view(), name='bulk-update-energy-data'),
    path('energy-data/bulk-delete/', EnergyDataDeleteView.as_view(), name='bulk-delete-energy-data'),
    path('carbon-offsets/', CarbonOffsetView.as_view(), name='carbon-offsets'),
    path('operational-metrics/', OperationalMetricView.as_view(), name='operational-metrics'),
]
