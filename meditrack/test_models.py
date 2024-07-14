from django.test import TestCase

from accounts.models import User
from medicine_app.models import Medicine, Person

class MyTestClass(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass
    
    def setUp(self) -> None:
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_one_plus_one_equals_two(self):
        print("Methods: test_one_plus_one_equals_two")
        self.assertEqual(1 + 1, 2)

class PersonModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create(username="Test User", password="Test Password")
        Person.objects.create(name="Test Person", user=user)
    
    def test_name_label(self):
        person = Person.objects.get(id=1)
        field_label = person._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        person = Person.objects.get(id=1)
        max_length = person._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)


class MedicineModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create(username="Test User", password="Test Password")
        person = Person.objects.create(name="Test Person", user=user)
        Medicine.objects.create(name="Test Medicine", doses=10, current_dose=5, person=person)

    def test_name_label(self):
        medicine = Medicine.objects.get(id=1)
        field_label = medicine._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        medicine = Medicine.objects.get(id=1)
        max_length = medicine._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_doses_label(self):
        medicine = Medicine.objects.get(id=1)
        field_label = medicine._meta.get_field("doses").verbose_name
        self.assertEqual(field_label, "doses")

    def test_current_dose_label(self):
        medicine = Medicine.objects.get(id=1)
        field_label = medicine._meta.get_field("current_dose").verbose_name
        self.assertEqual(field_label, "current dose")
