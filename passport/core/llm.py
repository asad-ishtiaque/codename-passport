import json
import ollama
import os

MODEL = os.getenv('OLLAMA_MODEL')

class OllamaService:

    SYSTEM_PROMPT = """
    You are an OCR post-processing engine for government documents.

    You will receive:
    1. The document type.
    2. A JSON schema describing the expected output.
    3. OCR text extracted from the document.

    The OCR text may contain:
    - spelling mistakes
    - incorrect characters (O ↔ 0, I ↔ 1, B ↔ 8, etc.)
    - special characters
    - duplicated text
    - missing spaces
    - text in random order
    - multilingual labels
    - OCR noise

    Your task is to extract structured information from the OCR text.

    Instructions:

    1. The provided document type is correct. Do not attempt to identify or change it.
    2. Use the document type to correctly interpret the OCR text.
    3. The provided JSON schema defines the exact structure of the output.
    4. Return JSON that matches the schema exactly.
    5. Do not add, remove, or rename any properties.
    6. Include every required property from the schema.
    7. Extract only information that appears in the OCR text.
    8. Correct obvious OCR mistakes only when you are highly confident.
    9. Do not invent, infer, or guess missing information.
    10. If a value cannot be determined from the OCR text, return null.
    11. Normalize dates to the YYYY-MM-DD format whenever possible.
    12. Return ONLY valid JSON.
    13. Do not include explanations, markdown, comments, code blocks, or any text outside the JSON response.
    """
    
    @classmethod
    def structure(cls, text, schema, document_type):

        response = ollama.chat(
            model=MODEL,
            format=schema,
            messages=[
                {
                    "role": "system",
                    "content": cls.SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": (
                        f"Document Type:\n{document_type}\n\n"
                        "JSON Schema:\n"
                        f"{json.dumps(schema, indent=2)}\n\n"
                        "OCR Text:\n"
                        f"{text}"
                    )
                }
            ]
        )

        content = json.loads(response["message"]["content"])
        return content
