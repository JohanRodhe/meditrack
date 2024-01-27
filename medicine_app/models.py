from django.db import models

# Create your models here.
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    doses = models.IntegerField()
    current_dose = models.IntegerField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=100)
    medicine = models.ForeignKey(Medicine, on_delete=models.DO_NOTHING)
    date = models.DateField()

    def __str__(self):
        return self.name
