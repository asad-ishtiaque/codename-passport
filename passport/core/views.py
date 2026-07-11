from django.views.generic import detail
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from passport.core.services import DocumentUploadService
import logging

logger = logging.getLogger(__name__)

class BaseDocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    model = None
    serializer_class = None

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        document = instance.document
        logger.info("DOCUMENT in perform_create: %s", document)
        text_data = DocumentUploadService.process_upload(
            document,
            document_type=self.model._meta.model_name,
            serializer_class=self.serializer_class,
        )
        logger.info("OCR data for %s: %s", self.model._meta.model_name, text_data)
