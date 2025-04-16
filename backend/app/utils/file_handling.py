import os
from pathlib import Path
from typing import Any
import logging

logger = logging.getLogger(__name__)
def allowed_file(filename):
    allowed_extensions = ["pdf", "png", "jpg", "jpeg"]

    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def save_uploaded_file(file: Any, upload_folder: Path) -> Path:
    """Saves the uploaded file to the specified folder.

    Args:
        file: The uploaded file.
        upload_folder: The folder to save the file to.
    """
    filepath: Path = Path()
    try:
        if file:  # and allowed_file(file.filename):
            filepath = upload_folder / Path(file.filename)
            file.save(filepath)
    except Exception as e:
        logger.error(f"Error saving uploaded file: {str(e)}", exc_info=True)

    else:
        return filepath
