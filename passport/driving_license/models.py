from django.db import models
from passport.core.models import IdentityDocumentBase
from passport.users.models import User


class DrivingLicense(IdentityDocumentBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='driving_license/')
    license_number = models.CharField(max_length=255)