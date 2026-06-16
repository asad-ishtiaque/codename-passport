from passport.core.validators import validate_document
from passport.core.ocr import EasyOCRService

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "pdf"]


class DocumentUploadService:
    @staticmethod
    def process_upload(document, document_type=None):
        """
        Runs the shared upload pipeline before the model FileField stores the
        document.
        """
        raw_ocr_data = EasyOCRService.extract(document)

        return raw_ocr_data


