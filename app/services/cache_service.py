# app/services/cache_service.py

"""
DAY-12 — Smart Caching Service
---------------------------------
This service provides:
- compute_hash(): creates unique fingerprint of a file/code block
- get_from_cache(): returns cached result if exists
- store_in_cache(): saves parsed/system results

Used to avoid re-parsing or re-analyzing unchanged files.
"""

import hashlib
import json
import os

CACHE_FOLDER = "cache_store"

# Create folder if missing
os.makedirs(CACHE_FOLDER, exist_ok=True)


# ----------------------------------------------------
# 1. Compute unique stable hash for any text content
# ----------------------------------------------------
def compute_hash(text: str) -> str:
    """
    Returns a SHA256 hash for a given text.
    Ensures same input → same hash.
    """
    if not isinstance(text, str):
        text = str(text)

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ----------------------------------------------------
# 2. Check if we already computed this content before
# ----------------------------------------------------
def get_from_cache(hash_value: str):
    """
    Returns cached JSON result if exists, else None.
    """
    file_path = os.path.join(CACHE_FOLDER, f"{hash_value}.json")

    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None


# ----------------------------------------------------
# 3. Save parsed or architecture result for future reuse
# ----------------------------------------------------
def store_in_cache(hash_value: str, data: dict):
    """
    Stores JSON-serializable data under cache/<hash>.json
    """
    file_path = os.path.join(CACHE_FOLDER, f"{hash_value}.json")

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"[CACHE ERROR] Could not write cache file: {e}")
