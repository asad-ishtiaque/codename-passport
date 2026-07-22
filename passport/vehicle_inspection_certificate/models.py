from django.db import models
from passport.core.models import DocumentBase
from passport.users.models import User

class VehicleInspectionCertificate(DocumentBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    certificate_number = models.CharField(max_length=255, blank=True, null=True)
    vehicle_model = models.CharField(max_length=255, blank=True, null=True)

