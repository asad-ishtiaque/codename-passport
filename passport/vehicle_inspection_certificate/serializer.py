from passport.core.serializer import BaseDocumentSerializer
from passport.vehicle_inspection_certificate.models import VehicleInspectionCertificate


class VehicleInspectionCertificateSerializer(BaseDocumentSerializer):
    class Meta:
        model = VehicleInspectionCertificate
        fields = "__all__"
        read_only_fields = ["user_id"] 
        