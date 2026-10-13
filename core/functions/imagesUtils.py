import os
import hashlib
import time


def get_hashed_file_path(instance, filename: str) -> str:

    ext = filename.split(".")[-1]

    unique_string = f"{filename}{time.time()}"

    filename_hash = hashlib.md5(unique_string.encode("utf-8")).hexdigest()

    return os.path.join("receipts_uploads/", f"{filename_hash}.{ext}")
