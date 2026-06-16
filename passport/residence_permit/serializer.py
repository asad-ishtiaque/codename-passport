from passport.core.serializer import BaseDocumentSerializer
from passport.residence_permit.models import ResidencePermit


class ResidencePermitSerializer(BaseDocumentSerializer):
    class Meta:
        model = ResidencePermit
        fields = "__all__"
        read_only_fields = ["user"]
