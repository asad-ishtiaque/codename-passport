from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.services import DocumentUploadService

class BaseDocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    model = None
    serializer_class = None

    def get_queryset(self):
        return self.model.objects.filter(
            user_id=self.request.user
        )


    def perform_create(self, serializer):
        file = self.request.FILES.get("file")
        DocumentUploadService.process_upload_file(file)
        serializer.save(user_id=self.request.user)
