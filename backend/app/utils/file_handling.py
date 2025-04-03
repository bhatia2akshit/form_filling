import os
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )

def save_uploaded_file(file):
    
    if file:  # and allowed_file(file.filename):
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        return filepath

    return None
