from django.db import models
from passport.core.models import IdentityDocumentBase
from passport.users.models import User


class DrivingLicense(IdentityDocumentBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=255, blank=True, null=True)
