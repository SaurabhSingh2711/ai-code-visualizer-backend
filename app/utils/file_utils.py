# app/utils/file_utils.py
import os
import uuid
from fastapi import UploadFile

TEMP_DIR = "temp_uploads"

def ensure_temp_dir():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR, exist_ok=True)

async def save_upload_file_temp(upload_file: UploadFile) -> str:
    """
    Save UploadFile to a temporary file and return its path.
    Caller is responsible for removing it when done.
    """
    ensure_temp_dir()
    ext = os.path.splitext(upload_file.filename)[1]
    fname = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(TEMP_DIR, fname)
    with open(path, "wb") as f:
        content = await upload_file.read()
        f.write(content)
    return path
