from rest_framework import serializers
from passport.core.validators import validate_document

class BaseDocumentSerializer(serializers.ModelSerializer):

    def validate_document(self, document):
        validate_document(document)
        return document

    class Meta:
        abstract = True