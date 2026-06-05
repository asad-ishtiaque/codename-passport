from django.db import models
from passport.core.models import IdentityDocumentBase
from passport.users.models import User

class ResidencePermit(IdentityDocumentBase):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    permit_number = models.CharField(max_length=255)
