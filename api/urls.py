from django.urls import path

from api.views.drones import DroneCreate, DroneAvailableList, DronesViewSet
from api.views.medications import MedicationListCreate

app_name = 'api'

urlpatterns = [
    path('medication/', MedicationListCreate.as_view()),
    path('drones/', DroneCreate.as_view()),
    path('drones/meds/<str:serial_number>/', DronesViewSet.as_view({'get': 'loaded_meds'}),
         name='drone_loaded_meds'),
    path('drones/battery/<str:serial_number>/', DronesViewSet.as_view({'get': 'battery_level'}),
         name='drone_battery_level'),
    path('drones/load/<str:serial_number>/', DronesViewSet.as_view({'post': 'load_drone'}),
         name='drone_load'),
    path('drones/available/', DroneAvailableList.as_view()),
]
