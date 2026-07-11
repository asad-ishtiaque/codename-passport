from passport.core.validators import validate_document
from passport.core.llm import OllamaService
from passport.core.ocr import RapidOCRService
import logging
logger = logging.getLogger(__name__)
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "pdf"]


class DocumentUploadService:
    @staticmethod
    def process_upload(document, document_type=None, serializer_class=None):
        """
        Runs the shared upload pipeline before the model FileField stores the
        document.
        """
        return DocumentUploadService.extract_information(
            document,
            document_type=document_type,
            serializer_class=serializer_class,
        )

    @staticmethod
    def extract_information(document, document_type=None, serializer_class=None):
        raw_ocr_data = RapidOCRService.extract(document)
        text_data = RapidOCRService.extract_text(raw_ocr_data)

        if serializer_class is None:
            logger.warning(
                "No serializer_class provided for %s; returning OCR text without LLM structuring.",
                document_type,
            )
            return text_data

        schema = serializer_class.extraction_schema()
        logger.info("Extraction schema for %s: %s", document_type, schema)

        return OllamaService.structure(text_data, schema=schema, document_type=document_type)

