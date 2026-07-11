from django.db import models
from passport.core.utils import document_upload_path

# DOCUMENT_TYPES = [
#         ("passport", "Passport"),
#         ("driving_license", "Driving License"),
#         ("vehicle_inspection_certificate", "Vehicle Inspection Certificate"),
#         ("residence_permit", "Residence Permit")
#     ]

class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    X = "X", "Unspecified"

class DocumentBase(models.Model):
    document = models.FileField(upload_to=document_upload_path)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    issue_date = models.DateField()
    issue_country = models.CharField(max_length=255)
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        abstract = True

class IdentityDocumentBase(DocumentBase):
    gender = models.CharField(max_length=1, choices=Gender.choices)
    nationality = models.CharField(max_length=255)

    class Meta:
        abstract = True