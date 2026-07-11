from rest_framework import serializers
from passport.core.validators import validate_document

class BaseDocumentSerializer(serializers.ModelSerializer):
    NON_EXTRACTABLE_FIELD_TYPES = (
        serializers.FileField,
        serializers.ImageField,
        serializers.HiddenField,
    )

    NON_EXTRACTABLE_FIELD_NAMES = {
        "id",
        "user",
        "document",
        "created_at",
        "updated_at",
    }

    def validate_document(self, document):
        validate_document(document)
        return document

    @classmethod
    def extraction_schema(cls):
        serializer = cls()
        properties = {}
        required = []

        for name, field in serializer.fields.items():
            if cls._should_skip_extraction_field(name, field):
                continue

            properties[name] = cls._json_schema_type(field)

            if field.required:
                required.append(name)

        return {
            "type": "object",
            "additionalProperties": False,
            "properties": properties,
            "required": required,
        }

    @classmethod
    def _should_skip_extraction_field(cls, name, field):
        return (
            name in cls.NON_EXTRACTABLE_FIELD_NAMES
            or field.read_only
            or field.write_only
            or isinstance(field, cls.NON_EXTRACTABLE_FIELD_TYPES)
        )
    
    @classmethod
    def _json_schema_type(cls, field):
        if isinstance(field, serializers.IntegerField):
            return {"type": "integer"}

        if isinstance(field, serializers.FloatField):
            return {"type": "number"}

        if isinstance(field, serializers.BooleanField):
            return {"type": "boolean"}

        if isinstance(field, serializers.DateField):
            return {
                "type": "string",
                "format": "date",
            }
        if isinstance(field, serializers.ChoiceField):
            return {
                "type": "string",
                "enum": list(field.choices.keys()),
        }

        return {"type": "string"}

    class Meta:
        abstract = True
