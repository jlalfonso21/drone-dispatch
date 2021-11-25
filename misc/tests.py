from django.core.exceptions import ValidationError
from django.test import TestCase

from misc.models import Drone


class DroneModelTests(TestCase):
    def test_failed_serial_number_field_drone_model_creation(self):
        obj = Drone(
            serial_number="#invalid",
            weight_limit=400,
            battery_capacity=100,
        )
        try:
            obj.full_clean()
        except ValidationError:
            self.assertTrue(True)
        else:
            self.fail("invalid serial number failed")

    def test_pass_serial_number_field_drone_model_creation(self):
        obj = Drone(
            serial_number="VALIDserial_number_cr34ti0n",
            weight_limit=400,
            battery_capacity=100,
        )
        try:
            obj.full_clean()
        except ValidationError:
            self.fail("valid serial number failed")
        else:
            self.assertTrue(True)

    def test_failed_weight_limit_field_drone_model_creation(self):
        obj = Drone.objects.create(
            serial_number="valid_serial_123",
            weight_limit=500.1,
            battery_capacity=100,
        )
        try:
            obj.full_clean()
        except ValidationError:
            self.assertTrue(True)
        else:
            self.fail("invalid weight limit failed")

    def test_pass_weight_limit_field_drone_model_creation(self):
        obj = Drone(
            serial_number="valid_serial_123",
            weight_limit=400,
            battery_capacity=100,
        )
        try:
            obj.full_clean()
        except ValidationError:
            self.fail("valid serial number failed")
        else:
            self.assertTrue(True)

    def test_failed__battery_capacity_field_drone_model_creation(self):
        obj = Drone.objects.create(
            serial_number="valid_serial_123",
            weight_limit=500,
            battery_capacity=101,
        )
        try:
            obj.full_clean()
        except ValidationError:
            self.assertTrue(True)
        else:
            self.fail("invalid battery capacity failed")

    def test_pass_battery_capacity_field_drone_model_creation(self):
        obj = Drone(
            serial_number="valid_serial_123",
            weight_limit=400,
            battery_capacity=100,
        )
        try:
            obj.full_clean()
        except ValidationError:
            self.fail("valid battery capacity failed")
        else:
            self.assertTrue(True)
