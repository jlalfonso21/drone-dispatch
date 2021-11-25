from django.db import models

DRONE_MODELS = (
    ('lightweight', 'Lightweight'),
    ('middleweight', 'Middleweight'),
    ('cruiserweight', 'Cruiserweight'),
    ('heavyweight', 'Heavyweight'),
)

DRONE_STATES = (
    ('IDLE', 'Idle'),
    ('LOADING', 'Loading'),
    ('LOADED', 'Loaded'),
    ('DELIVERING', 'Delivering'),
    ('DELIVERED', 'Delivered'),
    ('RETURNING', 'Returning'),
)


class Drone(models.Model):
    serial_number = models.CharField(max_length=100)
    model = models.CharField(max_length=20, choices=DRONE_MODELS, default='middleweight')
    weight_limit = models.FloatField()
    battery_capacity = models.FloatField()
    state = models.CharField(max_length=20, choices=DRONE_STATES)

    def __str__(self):
        return self.serial_number


class Medication(models.Model):
    name = models.CharField(max_length=255)
    weight = models.FloatField()
    code = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/medications')

    def __str__(self):
        return self.name
