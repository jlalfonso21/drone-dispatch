from django.core.exceptions import ValidationError
from django.test import TestCase

from misc.models import Medication


class MedicationModelTests(TestCase):
    def test_failed_name_field_model_creation(self):
        obj = Medication(
            name="#invalid",
            weight=400,
            code="100",
        )
        try:
            obj.full_clean()
        except ValidationError:
            self.assertTrue(True)
        else:
            self.fail("invalid name failed")

    def test_pass_name_field_model_creation(self):
        obj = Medication(
            name="valid_name-for-m3d1c4ti0n",
            weight=400,
            code="100",
        )
        try:
            obj.full_clean()
        except ValidationError:
            self.fail("valid code failed")
        else:
            self.assertTrue(True)

    def test_failed_code_field_model_creation_1(self):
        obj = Medication(
            name="valid_name-for-m3d1c4ti0n",
            weight=400,
            code="invalid code",
        )
        try:
            obj.full_clean()
        except ValidationError:
            self.assertTrue(True)
        else:
            self.fail("invalid code failed")

    def test_failed_code_field_model_creation_2(self):
        obj = Medication(
            name="valid_name-for-m3d1c4ti0n",
            weight=400,
            code="INVALID CODE",
        )
        try:
            obj.full_clean()
        except ValidationError:
            self.assertTrue(True)
        else:
            self.fail("invalid code failed")

    def test_failed_code_field_model_creation_3(self):
        obj = Medication(
            name="valid_name-for-m3d1c4ti0n",
            weight=400,
            code="INVALID-CODE",
        )
        try:
            obj.full_clean()
        except ValidationError:
            self.assertTrue(True)
        else:
            self.fail("invalid code failed")

    def test_pass_code_field_model_creation(self):
        obj = Medication(
            name="valid_name-for-m3d1c4ti0n",
            weight=400,
            code="V4L1D_M3D_C0D3",
        )
        try:
            obj.full_clean()
        except ValidationError:
            self.fail("valid name failed")
        else:
            self.assertTrue(True)
