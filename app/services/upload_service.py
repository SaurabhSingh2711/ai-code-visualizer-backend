import os
from pathlib import Path
from fastapi import UploadFile


class UploadService:
    """Stub UploadService for now."""

    @staticmethod
    def save_file(upload_dir: str, file: UploadFile) -> str:
        os.makedirs(upload_dir, exist_ok=True)
        dest = Path(upload_dir) / file.filename
        with open(dest, "wb") as f:
            f.write(file.file.read())
        return str(dest)

    @staticmethod
    def save_zip_and_extract(upload_dir: str, file: UploadFile) -> str:
        os.makedirs(upload_dir, exist_ok=True)
        zip_path = Path(upload_dir) / file.filename
        with open(zip_path, "wb") as f:
            f.write(file.file.read())
        return str(zip_path)
