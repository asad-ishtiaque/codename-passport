from passport.core.serializer import BaseDocumentSerializer
from passport.passport.models import Passport


class PassportSerializer(BaseDocumentSerializer):
    class Meta:
        model = Passport
        fields = "__all__"
        read_only_fields = ["user"]
