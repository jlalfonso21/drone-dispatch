from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

from api.errors import WeightError

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
    serial_number = models.CharField(max_length=100, unique=True,
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

    def set_idle_state(self):
        self.state = "IDLE"
        self.save()

    def set_loading_state(self):
        if self.state == "IDLE":
            self.state = "LOADING"
            self.save()

    def set_loaded_state(self):
        if self.state == "LOADING":
            self.state = "LOADED"
            self.save()

    def set_delivering_state(self):
        self.state = "DELIVERING"
        self.save()

    def set_delivered_state(self):
        self.state = "DELIVERED"
        self.save()

    def set_returning_state(self):
        self.state = "RETURNING"
        self.save()

    def get_or_create_cargo(self):
        try:
            cargo = self.cargo
        except:
            cargo = Cargo.objects.create(drone=self)
        return cargo

    def add_med(self, med, qty):
        if not self.cargo:
            cargo = Cargo.objects.create(drone=self)
        else:
            cargo = self.cargo
        cargo.add(med, qty)

    def remove_med(self, med, qty):
        if self.cargo:
            self.cargo.remove(med, qty)

    def clean_cargo(self):
        self.cargo.clean_drone()


class Medication(models.Model):
    name = models.CharField(max_length=255,
                            validators=(
                                RegexValidator(
                                    regex="^[a-zA-Z0-9]([a-zA-Z0-9_-])+$",
                                    message='Enter a valid value. '
                                            'Allowed only letters, underscores, dashes and numbers.'
                                ),
                            ))

    weight = models.FloatField(validators=[MinValueValidator(0), ], help_text="Weight in grams (g).")

    code = models.CharField(max_length=255,
                            validators=(
                                RegexValidator(
                                    regex="^[A-Z0-9]([A-Z0-9_])+$",
                                    message='Enter a valid value. '
                                            'Allowed only upper case letters, underscores and numbers.'
                                ),
                            ), unique=True)

    image = models.ImageField(upload_to='images/medications', null=True, blank=True)

    def __str__(self):
        return self.name


class CargoItem(models.Model):
    cargo = models.ForeignKey(to="misc.Cargo", on_delete=models.SET_NULL, null=True, related_name="items")
    med = models.ForeignKey(to="misc.Medication", on_delete=models.SET_NULL, null=True)
    qty = models.PositiveIntegerField(default=0)

    def weight(self):
        if not self.med:
            return 0
        return self.med.weight * self.qty


class Cargo(models.Model):
    drone = models.OneToOneField(to="misc.Drone", related_name="cargo", on_delete=models.SET_NULL, null=True)

    def clean_drone(self):
        self.drone = None
        self.save()

    def get_total_weight(self):
        return sum([i.weight() for i in self.items.all()])

    def can_load_this_weight(self, weight):
        return bool(
            self.drone and self.drone.weight_limit >= 0 and weight >= 0 and
            self.drone.weight_limit >= self.get_total_weight() + weight
        )

    def can_load_this_weight_list(self, weight_list):
        weight = sum(i for i in weight_list)
        return bool(
            self.drone and self.drone.weight_limit >= 0 and weight >= 0 and
            self.drone.weight_limit >= self.get_total_weight() + weight
        )

    def get_med_list(self):
        return [i.med for i in self.items.all()]

    def add(self, med, qty):
        items = self.items.all()
        meds = self.get_med_list()
        if not self.can_load_this_weight(med.weight * qty):
            raise WeightError("Can't load this weight.")
        if med in meds:
            for i in items:
                if i.med == med:
                    i.qty += qty
                    i.save()
        else:
            CargoItem.objects.create(cargo=self, med=med, qty=qty)

    def remove(self, med, qty):
        items = self.items.all()
        meds = self.get_med_list()
        if med in meds:
            for i in items:
                if i.med == med:
                    saved = False
                    if i.qty - qty >= 0:
                        i.qty -= qty
                        saved = True
                    if i.qty == 0:
                        i.delete()
                    else:
                        i.save() if saved else None
                    return
