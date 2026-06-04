from django.db import models
from passport.users.models import User


class Passport(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='passport/')
    passport_number = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    expiry_date = models.DateField()
    issue_date = models.DateField()
    issue_country = models.CharField(max_length=255)
    issue_state = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=255)