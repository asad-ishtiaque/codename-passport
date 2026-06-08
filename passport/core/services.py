import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from passport.core.validators import validate_document
from rest_framework.response import Response


ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "pdf"]


class DocumentUploadService:
    @staticmethod
    def save_file(file, folder="documents"):
        """
        Saves file to storage and returns path
        """
        path = f"{folder}/{file.name}"
        saved_path = default_storage.save(path, ContentFile(file.read()))

        return saved_path

    @staticmethod
    def process_upload_file(file):
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        validate_document(file)
        DocumentUploadService.save_file(file)
