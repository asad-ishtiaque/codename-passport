from django.core.exceptions import ValidationError
import os

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}

def validate_document(file):
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            "Only PDF, JPG, JPEG and PNG files are allowed."
        )