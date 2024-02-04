from django.db import models
from django.contrib.auth.models import AbstractUser

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    doses = models.IntegerField()
    current_dose = models.IntegerField()

    def __str__(self):
        return self.name

class MedicineEvent(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.DO_NOTHING)
    date = models.DateField()
    doses = models.IntegerField()

    def __str__(self):
        return self.name

class OtherEvent(models.Model):
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=100)
    medications = models.ForeignKey(Medicine, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



 

