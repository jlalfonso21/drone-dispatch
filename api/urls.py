from django.urls import path

from api.views.drones import DroneCreate, DroneAvailableList, DronesViewSet
from api.views.medications import MedicationListCreate

app_name = 'api'

urlpatterns = [
    path('medication/', MedicationListCreate.as_view()),
    path('drones/', DroneCreate.as_view()),
    path('drones/battery/<str:serial_number>/', DronesViewSet.as_view({'get': 'battery_level'}),
         name='drone_battery_level'),
    path('drones/available/', DroneAvailableList.as_view()),
]
