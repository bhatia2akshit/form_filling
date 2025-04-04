from flask import Blueprint, request, jsonify, Response
import os
import logging

from .services.document_analysis import load_combined_json, analyze_document

api = Blueprint("api", __name__)
logger = logging.getLogger(__name__)


@api.route("/get-combine-info", methods=["GET"])
def load_json_objects_route() -> tuple[Response, int]:
    """Intended Functionality: Gets the combined json object for the current user from the database.
    Current Functionality: Returns a the combined json object from the folder.

    """
    logger.info("Received request for combined JSON objects")
    try:
        summarized_data = load_combined_json()

        if len(summarized_data) == 0:
            logger.warning("No combined JSON found")
            return jsonify({"message": "No combined JSON found"}), 205

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
def analyze_document_route() -> tuple[Response, int]:
    logger.info("Received document analysis request")
    if "files" not in request.files:
        logger.warning("No file part in request")
        return jsonify({"error": "No file part"}), 400

    file = request.files["files"]
    try:
        analyze_document(file)

        logger.info("Document analysis completed successfully")
        return jsonify({"status": "success", "message": "Analysis completed"}), 200

    except Exception as e:
        logger.error(f"Error during document analysis: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
