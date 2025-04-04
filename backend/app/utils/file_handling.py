import os
from werkzeug.utils import secure_filename


def allowed_file(filename):
    allowed_extensions = ["pdf", "png", "jpg", "jpeg"]

    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def save_uploaded_file(file, upload_folder):
    if file:  # and allowed_file(file.filename):
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)
        return filepath

    return None
