from passport.core.views import BaseDocumentViewSet
from passport.passport.models import Passport
from passport.passport.serializer import PassportSerializer

class PasspportView(BaseDocumentViewSet):
    model = Passport
    serializer_class = PassportSerializer