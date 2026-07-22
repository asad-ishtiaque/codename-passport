from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from passport.driving_license.serializer import DrivingLicenseSerializer
from passport.passport.serializer import PassportSerializer
from passport.core.llm import OllamaService
from passport.core.models import DocumentStatus
from passport.core.serializer import DocumentUploadSerializer
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
    def test_create_uses_upload_serializer(self):
        viewset = BaseDocumentViewSet()
        viewset.action = "create"
        viewset.model = SimpleNamespace(__name__="Passport")

        serializer_class = viewset.get_serializer_class()

        assert issubclass(serializer_class, DocumentUploadSerializer)
        assert serializer_class.Meta.model == viewset.model
        assert serializer_class.Meta.fields == ["document"]

    def test_perform_create_processes_document_and_saves_extracted_fields(self):
        document = SimpleUploadedFile(
            "passport.pdf",
            b"%PDF-1.4",
            content_type="application/pdf",
        )
        instance = Mock(document=document)
        serializer = Mock(validated_data={"document": document})
        serializer.save.return_value = instance
        user = SimpleNamespace(id="user-id")
        extraction_serializer = Mock()

        viewset = BaseDocumentViewSet()
        viewset.request = SimpleNamespace(user=user)
        viewset.format_kwarg = None
        viewset.model = SimpleNamespace(
            _meta=SimpleNamespace(model_name="passport"),
        )
        viewset.serializer_class = Mock(return_value=extraction_serializer)

        with patch.object(
            DocumentUploadService,
            "process_upload",
            return_value={"first_name": "Ada"},
        ) as process_upload:
            viewset.perform_create(serializer)

        process_upload.assert_called_once_with(
            document,
            document_type="passport",
            serializer_class=viewset.serializer_class,
        )
        serializer.save.assert_called_once_with(user=user)
        instance.save.assert_any_call(update_fields=["status", "updated_at"])
        assert instance.status == DocumentStatus.PROCESSING
        viewset.serializer_class.assert_called_once_with(
            instance=instance,
            data={"first_name": "Ada"},
            partial=True,
            context=viewset.get_serializer_context(),
        )
        extraction_serializer.is_valid.assert_called_once_with(raise_exception=True)
        extraction_serializer.save.assert_called_once_with(status=DocumentStatus.EXTRACTED)

    def test_perform_create_marks_document_failed_when_processing_fails(self):
        document = SimpleUploadedFile(
            "passport.pdf",
            b"%PDF-1.4",
            content_type="application/pdf",
        )
        instance = Mock(document=document)
        serializer = Mock(validated_data={"document": document})
        serializer.save.return_value = instance
        user = SimpleNamespace(id="user-id")

        viewset = BaseDocumentViewSet()
        viewset.request = SimpleNamespace(user=user)
        viewset.model = SimpleNamespace(
            _meta=SimpleNamespace(model_name="passport"),
        )
        viewset.serializer_class = PassportSerializer

        with patch.object(
            DocumentUploadService,
            "process_upload",
            side_effect=ValueError("bad OCR"),
        ):
            with self.assertRaises(ValueError):
                viewset.perform_create(serializer)

        serializer.save.assert_called_once_with(user=user)
        assert instance.status == DocumentStatus.FAILED
        instance.save.assert_called_with(update_fields=["status", "updated_at"])

    def test_extraction_schema_uses_document_serializer_fields(self):
        passport_schema = PassportSerializer.extraction_schema()
        driving_license_schema = DrivingLicenseSerializer.extraction_schema()

        assert "passport_number" in passport_schema["properties"]
        assert passport_schema["properties"]["passport_number"] == {"type": "string"}
        assert "license_number" not in passport_schema["properties"]

        assert "license_number" in driving_license_schema["properties"]
        assert driving_license_schema["properties"]["license_number"] == {"type": "string"}
        assert "passport_number" not in driving_license_schema["properties"]

    def test_extraction_schema_excludes_non_ocr_fields(self):
        schema = VehicleInspectionCertificateSerializer.extraction_schema()

        assert "certificate_number" in schema["properties"]
        assert "vehicle_model" in schema["properties"]
        assert "document" not in schema["properties"]
        assert "status" not in schema["properties"]
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
