import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    UPLOAD_FOLDER = "./uploads"
    JSON_FOLDER = "./json_objects"
    COMBINED_JSON_FOLDER = "./combined_json_objects"
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # Azure Document Intelligence
    AZURE_ENDPOINT = "https://infoextraction.cognitiveservices.azure.com/"
    AZURE_KEY = "CzJ4i5wO1cmA2nRMbQ3GaRbDiLUoPpZAvFERRqpKZ2ldClLVvpwnJQQJ99BCAC1i4TkXJ3w3AAALACOGXf2j"

    @staticmethod
    def init_app(app):
        # Ensure upload folder exists
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        os.makedirs(app.config["JSON_FOLDER"], exist_ok=True)
        os.makedirs(app.config["COMBINED_JSON_FOLDER"], exist_ok=True)
