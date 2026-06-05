from rest_framework import serializers


class BaseDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True