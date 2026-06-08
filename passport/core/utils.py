import uuid
import os

def document_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"{instance._meta.model_name}/{uuid.uuid4()}{ext}"