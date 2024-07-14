from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts.models import User

class Person(models.Model):
    """
    Represents a person in the system.
    """

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.name)

class Medicine(models.Model):
    """
    Represents a medicine in the system.

    Attributes:
        name (str): The name of the medicine.
        doses (int): The total number of doses for the medicine.
        current_dose (int): The current dose of the medicine.

    Methods:
        __str__(): Returns a string representation of the medicine.
    """
    name = models.CharField(max_length=100)
    doses = models.IntegerField()
    current_dose = models.IntegerField()
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.name)

class MedicineEvent(models.Model):
    """
    Represents an event related to a medicine, such as a dosage or administration.

    Attributes:
        medicine (Medicine): The medicine associated with the event.
        date (DateField): The date of the event.
        doses (IntegerField): The number of doses administered.

    Methods:
        __str__(): Returns a string representation of the medicine event.
    """
    medicine = models.ForeignKey(Medicine, on_delete=models.DO_NOTHING)
    date = models.DateField()
    doses = models.IntegerField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.medicine.name

    @classmethod
    def create_event(cls, person, medicine, date, doses):
        event = cls(person=person, medicine=medicine, date=date, doses=doses)
        event.save()
        medicine.current_dose += doses
        medicine.save()
        return event

class OtherEvent(models.Model):
    """
    Represents an event other than medication in the application.
    """

    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return str(self.title)




 

