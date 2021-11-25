from django.urls import path

from api.views.drones import DroneCreate, DroneAvailableList
from api.views.medications import MedicationListCreate

app_name = 'api'

urlpatterns = [
    path('medication/', MedicationListCreate.as_view()),
    path('drones/', DroneCreate.as_view()),
    path('drones/available/', DroneAvailableList.as_view()),
]
