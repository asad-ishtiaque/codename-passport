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

class DocumentStatus(models.TextChoices):
    UPLOADED = "UPLOADED", "Uploaded"
    PROCESSING = "PROCESSING", "Processing"
    EXTRACTED = "EXTRACTED", "Extracted"
    FAILED = "FAILED", "Failed"

class DocumentBase(models.Model):
    document = models.FileField(upload_to=document_upload_path)
    status = models.CharField(
        max_length=20,
        choices=DocumentStatus.choices,
        default=DocumentStatus.UPLOADED,
    )
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    issue_country = models.CharField(max_length=255, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        abstract = True

class IdentityDocumentBase(DocumentBase):
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True
