from django.db import models

class DocumentBase(models.Model):
    image = models.ImageField(upload_to='documentBase/')
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
    gender = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)

    class Meta:
        abstract = True