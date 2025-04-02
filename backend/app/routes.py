from flask import Blueprint, request, jsonify, current_app, Response
import os

from .utils.file_handling import save_uploaded_file
from .services.document_analysis import DocumentAnalysisService

api = Blueprint("api", __name__)
documentAnalysisService = DocumentAnalysisService()


@api.route("/combine-info", methods=["GET"])
def combine_json_objects() -> tuple[Response, int]:
    """Intended Functionality: Gets the combined json object for the current user from the database.
    Current Functionality: Returns a the combined json object from the folder.

    """
    try:
        summarized_data = documentAnalysisService.summarize_jsons()
        return (
            jsonify(
                {
                    "status": "success",
                    "data": summarized_data,  # The actual data to display
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify(
            {"status": "error", "message": f"Failed to combine JSONs: {str(e)}"}
        ), 500


@api.route("/health", methods=["GET"])
def check_health():
    return jsonify({"status": "healthy"}), 200


@api.route("/analyze-documents", methods=["POST"])
def analyze_document() -> tuple[Response, int]:

    if "files" not in request.files:
        print("is file not found?")
        return jsonify({"error": "No file part"}), 400

    file = request.files["files"]
    try:
        # Save the uploaded file
        file_path = save_uploaded_file(file)

        if not file_path:
            print("file path not good")
            return jsonify({"error": "Invalid file type"}), 400

        # Analyze the document
        documentAnalysisService.analyze_document(file_path)

        try:
            os.remove(file_path)
        except:
            pass
        return jsonify({"status": "success", "message": "Analysis completed"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@api.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200
