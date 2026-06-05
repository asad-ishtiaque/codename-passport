from passport.core.serializer import BaseDocumentSerializer
from passport.driving_license.models import DrivingLicense


class DrivingLicenseSerializer(BaseDocumentSerializer):
    class Meta:
        model = DrivingLicense
        fields = "__all__"
        read_only_fields = ["user_id"]
