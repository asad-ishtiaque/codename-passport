from django.views.generic import detail
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from passport.core.models import DocumentStatus
from passport.core.serializer import DocumentUploadSerializer
from passport.core.services import DocumentUploadService
import logging
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

class BaseDocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    model = None
    serializer_class = None
    upload_serializer_class = DocumentUploadSerializer

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user
        )

    def get_upload_serializer_class(self):
        if hasattr(self, "_upload_serializer_class"):
            return self._upload_serializer_class
        class UploadSerializer(self.upload_serializer_class):
            class Meta(self.upload_serializer_class.Meta):
                model = self.model
                fields = ["document"]

        self._upload_serializer_class = UploadSerializer
        return UploadSerializer

    def get_serializer_class(self):
        if getattr(self, "action", None) == "create":
            return self.get_upload_serializer_class()

        return self.serializer_class


    def create(self, request, *args, **kwargs):
        upload_serializer = self.get_serializer(data=request.data)
        upload_serializer.is_valid(raise_exception=True)

        instance = upload_serializer.save(
            user=request.user,
            status=DocumentStatus.PROCESSING,
        )

        try:
            extracted_data = DocumentUploadService.process_upload(
                document=instance.document,
                document_type=self.model._meta.model_name,
                serializer_class=self.serializer_class,
            )

            serializer = self.serializer_class(
                instance=instance,
                data=extracted_data,
                partial=True,
            )

            serializer.is_valid(raise_exception=True)
            instance = serializer.save(status=DocumentStatus.EXTRACTED)

        except Exception:
            instance.status = DocumentStatus.FAILED
            instance.save(update_fields=["status"])
            raise

        return Response(
            self.serializer_class(instance).data,
            status=status.HTTP_201_CREATED,
        )