from flask import Blueprint, request, jsonify, current_app, Response
import os
import logging

from .utils.file_handling import save_uploaded_file
from .services.document_analysis import DocumentAnalysisService

api = Blueprint("api", __name__)
documentAnalysisService = None
logger = logging.getLogger(__name__)


def get_document_analysis_service():
    global documentAnalysisService
    if documentAnalysisService is None:
        logger.info("Initializing DocumentAnalysisService")
        documentAnalysisService = DocumentAnalysisService(current_app.config)
    return documentAnalysisService


@api.route("/get-combine-info", methods=["GET"])
def load_json_objects() -> tuple[Response, int]:
    """Intended Functionality: Gets the combined json object for the current user from the database.
    Current Functionality: Returns a the combined json object from the folder.

    """
    logger.info("Received request for combined JSON objects")
    try:
        service = get_document_analysis_service()
        summarized_data = service.load_combined_json()

        if len(summarized_data) is 0:
            logger.warning("No combined JSON found")
            return jsonify({"message": "No combined JSON found"}), 404

        logger.info("Successfully retrieved combined JSON data")
        return (
            jsonify(
                {
                    "data": summarized_data,  # The actual data to display
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Error retrieving combined JSON: {str(e)}", exc_info=True)
        return jsonify(
            {
                "status": "error",
                "message": f"Failed to retrieve combined JSON: {str(e)}",
            }
        ), 500


@api.route("/health", methods=["GET"])
def check_health() -> tuple[Response, int]:
    logger.debug("Health check endpoint called")
    return jsonify({"status": "healthy"}), 200


@api.route("/analyze-documents", methods=["POST"])
def analyze_document() -> tuple[Response, int]:
    logger.info("Received document analysis request")
    if "files" not in request.files:
        logger.warning("No file part in request")
        return jsonify({"error": "No file part"}), 400

    file = request.files["files"]
    try:
        # Save the uploaded file
        logger.info("Saving uploaded file")
        file_path = save_uploaded_file(file)

        if not file_path:
            logger.error("Invalid file type received")
            return jsonify({"error": "Invalid file type"}), 400

        # Analyze the document
        logger.info(f"Starting document analysis for file: {file_path}")
        service = get_document_analysis_service()
        service.analyze_document(file_path)

        try:
            logger.info(f"Cleaning up temporary file: {file_path}")
            os.remove(file_path)
        except Exception as e:
            logger.warning(f"Failed to remove temporary file: {str(e)}")

        logger.info("Document analysis completed successfully")
        return jsonify({"status": "success", "message": "Analysis completed"}), 200

    except Exception as e:
        logger.error(f"Error during document analysis: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
