from django.db import models
from passport.users.models import User
from passport.core.models import IdentityDocumentBase


class Passport(IdentityDocumentBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passport_number = models.CharField(max_length=255, blank=True, null=True)
    issue_state = models.CharField(max_length=255, blank=True, null=True)
