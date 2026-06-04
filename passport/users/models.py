import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Gender(models.TextChoices):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=255, choices=Gender.choices, default=Gender.MALE)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255)

    groups = None
    user_permissions = None

    def __str__(self):
        return self.username
