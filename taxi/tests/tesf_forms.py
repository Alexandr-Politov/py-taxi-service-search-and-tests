from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, SearchForm


class DriverFormTest(TestCase):
    def test_driver_creation_form(self) -> None:
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "Testfirst",
            "last_name": "Testsecond",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form(self) -> None:
        form_data = {"license_number": "ABC54321"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.changed_data, ["license_number"])

    def test_driver_license_update_form_invalid(self) -> None:
        form_data = {"license_number": "123test"}
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class TestSearchForms(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword",
            first_name="TestFirst",
            last_name="TestSecond",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer
        )

    def test_search_form(self) -> None:
        form_data = {"username": "test"}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        drivers = get_user_model().objects.filter(
            username__icontains=form_data["username"]
        )
        self.assertEqual(list(drivers), [self.driver])
