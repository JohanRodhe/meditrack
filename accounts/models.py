from django.db import models
from django.contrib.auth.models import AbstractUser
from medicine_app.models import Person

# Create your models here
class User(AbstractUser):
    pass

