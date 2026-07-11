from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from passport.driving_license.serializer import DrivingLicenseSerializer
from passport.passport.serializer import PassportSerializer
from passport.core.llm import OllamaService
from passport.core.services import DocumentUploadService
from passport.core.views import BaseDocumentViewSet
from passport.vehicle_inspection_certificate.serializer import (
    VehicleInspectionCertificateSerializer,
)


class DocumentUploadServiceTests(SimpleTestCase):
    def test_process_upload_validates_and_extracts_information(self):
        document = SimpleUploadedFile(
            "passport.pdf",
            b"%PDF-1.4",
            content_type="application/pdf",
        )

        with patch.object(
            DocumentUploadService,
            "extract_information",
            return_value={"first_name": "Ada"},
        ) as extract_information:
            result = DocumentUploadService.process_upload(
                document,
                document_type="passport",
            )

        assert result == {"first_name": "Ada"}
        extract_information.assert_called_once_with(
            document,
            document_type="passport",
            serializer_class=None,
        )


class BaseDocumentViewSetTests(SimpleTestCase):
    def test_perform_create_processes_document_and_saves_authenticated_user(self):
        document = SimpleUploadedFile(
            "passport.pdf",
            b"%PDF-1.4",
            content_type="application/pdf",
        )
        serializer = Mock(validated_data={"document": document})
        user = SimpleNamespace(id="user-id")

        viewset = BaseDocumentViewSet()
        viewset.request = SimpleNamespace(user=user)
        viewset.model = SimpleNamespace(
            _meta=SimpleNamespace(model_name="passport"),
        )
        viewset.serializer_class = PassportSerializer

        with patch.object(DocumentUploadService, "process_upload") as process_upload:
            viewset.perform_create(serializer)

        process_upload.assert_called_once_with(
            document,
            document_type="passport",
            serializer_class=PassportSerializer,
        )
        serializer.save.assert_called_once_with(user=user)

    def test_extraction_schema_uses_document_serializer_fields(self):
        passport_schema = PassportSerializer.extraction_schema()
        driving_license_schema = DrivingLicenseSerializer.extraction_schema()

        assert "passport_number" in passport_schema["properties"]
        assert passport_schema["properties"]["passport_number"] == {}
        assert "license_number" not in passport_schema["properties"]

        assert "license_number" in driving_license_schema["properties"]
        assert driving_license_schema["properties"]["license_number"] == {}
        assert "passport_number" not in driving_license_schema["properties"]

    def test_extraction_schema_excludes_non_ocr_fields(self):
        schema = VehicleInspectionCertificateSerializer.extraction_schema()

        assert "certificate_number" in schema["properties"]
        assert "vehicle_model" in schema["properties"]
        assert "document" not in schema["properties"]
        assert "user" not in schema["properties"]
        assert "created_at" not in schema["properties"]
        assert "updated_at" not in schema["properties"]


class OllamaServiceTests(SimpleTestCase):
    def test_normalize_to_schema_drops_extra_keys_and_fills_missing_keys(self):
        schema = {
            "properties": {
                "passport_number": {},
                "first_name": {},
                "expiry_date": {},
            }
        }

        result = OllamaService._normalize_to_schema(
            {
                "passport_number": "A1234567",
                "first_name": "Ada",
                "invented_key": "ignored",
            },
            schema,
        )

        assert result == {
            "passport_number": "A1234567",
            "first_name": "Ada",
            "expiry_date": None,
        }
