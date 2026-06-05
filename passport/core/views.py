from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class BaseDocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    model = None
    serializer_class = None

    def get_queryset(self):
        return self.model.objects.filter(
            user_id=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)