# app/utils/file_utils.py
import os
import uuid
import zipfile
import shutil
from fastapi import UploadFile

TEMP_DIR = "temp_uploads"


def ensure_temp_dir():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR, exist_ok=True)


async def save_upload_file_temp(upload_file: UploadFile) -> str:
    """
    Save single UploadFile to a temporary file and return its path.
    """
    ensure_temp_dir()
    ext = os.path.splitext(upload_file.filename)[1]
    fname = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(TEMP_DIR, fname)

    with open(path, "wb") as f:
        content = await upload_file.read()
        f.write(content)

    return path


# --------------------------------------------------------------------
# NEW — DAY-8 ZIP SUPPORT
# --------------------------------------------------------------------

def extract_zip_to_temp(upload_file: UploadFile) -> str:
    """
    Extract uploaded ZIP to a temp folder and return the folder path.
    """
    ensure_temp_dir()

    # create unique folder for extraction
    extract_dir = os.path.join(TEMP_DIR, uuid.uuid4().hex)
    os.makedirs(extract_dir, exist_ok=True)

    # save uploaded zip temporarily
    zip_temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}.zip")
    with open(zip_temp_path, "wb") as f:
        f.write(upload_file.file.read())

    # extract
    with zipfile.ZipFile(zip_temp_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    # remove the temporary zip
    os.remove(zip_temp_path)

    return extract_dir


def cleanup_temp_dir(path: str):
    """
    Remove extracted ZIP folder.
    """
    try:
        shutil.rmtree(path)
    except Exception:
        pass
