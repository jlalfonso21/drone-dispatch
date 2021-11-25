from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
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
    serial_number = models.CharField(max_length=100,
                                     validators=(
                                         RegexValidator(
                                             regex="^[a-zA-Z0-9]([a-zA-Z0-9_-])+$",
                                             message='Enter a valid value. '
                                                     'Allowed only letters, underscores, dashes and numbers.'
                                         ),
                                     ))

    model = models.CharField(max_length=20, choices=DRONE_MODELS, default='middleweight')

    weight_limit = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(500), ],
                                     help_text="Weight in grams (g). 500g max.")

    battery_capacity = models.FloatField(default=100.0, validators=[MinValueValidator(0), MaxValueValidator(100), ])

    state = models.CharField(max_length=20, choices=DRONE_STATES, default='IDLE')

    def __str__(self):
        return self.serial_number


class Medication(models.Model):
    name = models.CharField(max_length=255)
    weight = models.FloatField()
    code = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/medications')

    def __str__(self):
        return self.name
