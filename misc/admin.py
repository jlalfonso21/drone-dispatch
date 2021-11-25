from django.contrib import admin

# Register your models here.
from misc.models import Medication, Drone

admin.site.register(Drone)
admin.site.register(Medication)
