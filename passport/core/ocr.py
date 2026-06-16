# passport/core/ocr.py

import easyocr
from pdf2image import convert_from_path
import logging

logger = logging.getLogger(__name__)


class EasyOCRService:
    reader = easyocr.Reader(["en"], gpu=False)

    @classmethod
    def extract(cls, document):
        logger.info("Document: %s", document)
        file_path = document.path

        if file_path.lower().endswith(".pdf"):
            return cls.extract_from_pdf(file_path)

        return cls.extract_from_image(file_path)

    @classmethod
    def extract_from_image(cls, file_path):
        results = cls.reader.readtext(file_path)

        return {
            "raw_text": "\n".join([text for _, text, _ in results]),
            "items": [
                {
                    "text": text,
                    "confidence": confidence,
                    "box": box,
                }
                for box, text, confidence in results
            ],
        }

    @classmethod
    def extract_from_pdf(cls, file_path):
        pages = convert_from_path(file_path)
        all_text = []
        all_items = []

        for page in pages:
            results = cls.reader.readtext(page)

            for box, text, confidence in results:
                all_text.append(text)
                all_items.append({
                    "text": text,
                    "confidence": confidence,
                    "box": box,
                })

        return {
            "raw_text": "\n".join(all_text),
            "items": all_items,
        }
