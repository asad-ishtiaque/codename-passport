from passport.core.views import BaseDocumentViewSet
from passport.passport.models import Passport
from passport.passport.serializer import PassportSerializer

class PasspportViewSet(BaseDocumentViewSet):
    model = Passport
    serializer_class = PassportSerializer
    