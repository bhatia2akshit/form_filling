from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import os
from azure.core.credentials import AzureKeyCredential
import json
from datetime import datetime
from pathlib import Path
import logging
from ..utils.file_handling import save_uploaded_file
import time

logger = logging.getLogger(__name__)


def load_config(file_path):
    config = {}
    if Path(file_path).exists():
        f = Path(file_path).open("r")
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                config[key.strip()] = value.strip()
    return config


config = load_config("./config.txt")
print(config)

# Global variables for configuration
_upload_folder = Path(config["UPLOAD_FOLDER"])
_json_folder = Path(config["JSON_FOLDER"])
_combined_json_folder = Path(config["COMBINED_JSON_FOLDER"])
_azure_endpoint = config["AZURE_ENDPOINT"]
_azure_key = config["AZURE_KEY"]
logger.debug("Document Analysis Service initialized with config")


def analyze_document(file) -> dict:
    try:
        # Save the uploaded file
        logger.info("Saving uploaded file")
        file_path = save_uploaded_file(file=file, upload_folder=_upload_folder)

        document_analysis_client = DocumentAnalysisClient(
            endpoint=_azure_endpoint,
            credential=AzureKeyCredential(_azure_key),
        )

        file_opened = Path(file_path).open("rb")

        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-document", file_opened
        )
        result = poller.result()
        logger.debug("The document is parsed.")

        formatted_result = {}
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                formatted_result[kv_pair.key.content] = kv_pair.value.content

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename: Path = Path(f"analysis_result_{timestamp}.json")
        output_path: Path = _json_folder / output_filename

        output_file = output_path.open("w")
        if len(formatted_result) == 0:
            logger.info("empty json object")
        else:
            logger.info(f"formatted_result: {formatted_result}")
            json.dump(formatted_result, output_file, indent=4)
            output_file.close()

        time.sleep(5)
        logger.info("Summarizing JSONs")
        summarize_jsons()

    # return formatted_result
    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        raise


def summarize_jsons() -> None:
    """Summarizes the json objects available in the json folder and make a unified json object"""

    # check if there is already an existing json object.
    contents = os.listdir(_combined_json_folder)
    old_combined_json: Path = None

    if len(contents) > 0:
        logger.info("loading the existing combined json object")
        old_combined_json: Path = _combined_json_folder / Path(contents[0])
        combined_json: dict = json.load(old_combined_json.open("r"))
    else:
        logger.info("no existing combined json object found")
        combined_json: dict = {}

    time.sleep(5)
    json_files: list[str] = os.listdir(_json_folder)
    logger.info(f"json_files: {json_files}")
    for file in json_files:
        json_file: dict = None
        if file.endswith(".json"):
            opened_file = (_json_folder / Path(file)).open("rb")

            content = opened_file.read()
            logger.info("content is: ", content)
            logger.info(f"content: {content}")
            # if not content.strip():
            #     logger.warning(f"Skipping empty file: {file}")
            #     continue
            try:
                json_file = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON from {file}: {str(e)}")
                continue

        if json_file:
            for key, value in json_file.items():
                # Strip whitespace from key and value if needed
                print(f"key: {key}, value: {value}")
                key: str = key.strip()
                value: str = value.strip()

                # if the key is already present in the combined json object, append the value to the existing value
                if key in combined_json:
                    logger.info(
                        f"key: {key} already present in the combined json object"
                    )
                    values = combined_json[key]
                    if value not in values:
                        combined_json[key].append(value)
                else:
                    logger.info(f"adding new key: {key} to the combined json object")
                    combined_json[key] = [value]

    logger.info("saving the combined json object")
    if len(combined_json) == 0:
        logger.info("empty combined json object")
    # save combined_json to the folder.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filepath = _combined_json_folder / Path(
        f"combined_analysis_result_{timestamp}.json"
    )
    output_file = output_filepath.open("w")
    json.dump(combined_json, output_file, indent=4)

    if old_combined_json:
        logger.debug(f"Removing old combined json file: {old_combined_json}")
        os.remove(old_combined_json)


def load_combined_json() -> dict:
    contents = os.listdir(_combined_json_folder)
    if len(contents) > 0:
        logger.debug("loading the combined json object")
        old_combined_json: Path = _combined_json_folder / Path(contents[0])
        return json.load(old_combined_json.open("r"))
    return {}
