from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from passport.core.services import DocumentUploadService
from passport.core.views import BaseDocumentViewSet


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

        with patch.object(DocumentUploadService, "process_upload") as process_upload:
            viewset.perform_create(serializer)

        process_upload.assert_called_once_with(
            document,
            document_type="passport",
        )
        serializer.save.assert_called_once_with(user=user)
