from passport.core.views import BaseDocumentViewSet
from passport.residence_permit.models import ResidencePermit
from passport.residence_permit.serializer import ResidencePermitSerializer

class ResidencePermitViewSet(BaseDocumentViewSet):
    model = ResidencePermit
    serializer_class = ResidencePermitSerializer
