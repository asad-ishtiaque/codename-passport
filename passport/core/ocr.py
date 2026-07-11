# passport/core/ocr.py

from rapidocr import RapidOCR
from pdf2image import convert_from_path
import logging

logger = logging.getLogger(__name__)

class RapidOCRService:
    engine = RapidOCR()

    @classmethod
    def extract(cls, document):
        file_path = document.path

        if file_path.lower().endswith(".pdf"):
            return cls.extract_from_pdf(file_path)

        return cls.extract_from_image(file_path)

    @classmethod
    def extract_from_image(cls, file_path):
        result = cls.engine(file_path)
        logger.info("Result from OCR: %s", result)
        return result


    @classmethod
    def extract_from_pdf(cls, file_path):
        pages = convert_from_path(file_path)
        all_text = []
        all_items = []

        for page in pages:
            result = cls.engine(page)
            logger.info("Result from OCR: %s", result)
            return result
    
    @staticmethod
    def extract_text(result):
        if result is None:
            return ""

        return "\n".join(result.txts)

    @staticmethod
    def extract_scores(result):
        if result is None:
            return ""
        return "\n".join(result.scores)
