# app/utils/file_utils.py

import os
import uuid
import shutil
import tempfile
from fastapi import UploadFile

TEMP_DIR = "temp_uploads"


def ensure_temp_dir():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR, exist_ok=True)


async def save_upload_file_temp(upload_file: UploadFile) -> str:
    """
    Saves the uploaded file WITHOUT consuming the file stream,
    so other functions can still read the content.
    """

    ensure_temp_dir()

    # Get extension (.py or .java)
    ext = os.path.splitext(upload_file.filename)[1]
    fname = f"{uuid.uuid4().hex}{ext}"
    temp_path = os.path.join(TEMP_DIR, fname)

    # Use raw file stream WITHOUT calling upload_file.read()
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # Reset file pointer so the caller can read again
    upload_file.file.seek(0)

    return temp_path
