from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import os
from azure.core.credentials import AzureKeyCredential
import json
from datetime import datetime
from pathlib import Path
import logging


logger = logging.getLogger(__name__)

class DocumentAnalysisService:
    def __init__(self, config: dict):
        self._upload_folder = Path(config["UPLOAD_FOLDER"])
        self._json_folder = Path(config["JSON_FOLDER"])
        self._combined_json_folder = Path(config["COMBINED_JSON_FOLDER"])
        logger.debug("DocumentAnalysisService initialized with config")
        self._azure_endpoint: str = config["AZURE_ENDPOINT"]
        self._azure_key: str = config["AZURE_KEY"]

    def analyze_document(self, file_path) -> dict:
        try:
            # document_analysis_client = DocumentAnalysisClient(
            #     endpoint=self._azure_endpoint,
            #     credential=AzureKeyCredential(self._azure_key),
            # )

            # file_opened = Path(file_path).open("rb")

            # poller = document_analysis_client.begin_analyze_document(
            #     "prebuilt-document", file_opened
            # )
            # result = poller.result()
            # logger.debug("The document is parsed.")

            # formatted_result = {}
            # for kv_pair in result.key_value_pairs:
            #     if kv_pair.key and kv_pair.value:
            #         formatted_result[kv_pair.key.content] = [kv_pair.value.content]
            #     else:
            #         formatted_result[kv_pair.key.content] = [kv_pair.key.content]

            # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # output_filename: Path = Path(f"analysis_result_{timestamp}.json")
            # output_path: Path = self._json_folder / output_filename

            # output_file = output_path.open("w")
            # logger.debug("Dumping parsed json")
            # json.dump(formatted_result, output_file, indent=4)

            # logger.debug("Summarizing JSONs")
            self.summarize_jsons()

            # return formatted_result
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            raise

    def summarize_jsons(self) -> None:
        """Summarizes the json objects available in the json folder and make a unified json object"""

        # check if there is already an existing json object.
        contents = os.listdir(self._combined_json_folder)
        old_combined_json: Path = None
        
        if len(contents) > 1:
            old_combined_json = self._combined_json_folder / Path(contents[0])
            combined_json: {} = json.load(old_combined_json.open("r"))

        else:
            combined_json: {} = {}

        logger.debug("loading the json files collected in json objects")
        json_files = os.listdir(self._json_folder)
        
        for file in json_files:
            json_file: dict = None
            if file.endswith(".json"):
                print(f"loading the json file: {self._json_folder / Path(file)}")
                opened_file = (self._json_folder / Path(file)).open("r")

                content = opened_file.read()
                if not content.strip():
                    logger.warning(f"Skipping empty file: {file}")
                    continue
                try:
                    json_file = json.loads(content)
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing JSON from {file}: {str(e)}")
                    continue

                if json_file:
                    for key, value in json_file.items():
                        # if the key is already present in the combined json object, append the value to the existing value
                        if key in combined_json:
                            if isinstance(value, list):
                                combined_json[key].extend(value)
                            else:
                                combined_json[key] = [combined_json[key], value]
                        else:
                            combined_json[key] = [value]
        
        logger.debug("saving the combined json object")
        logger.debug(combined_json)
        # save combined_json to the folder.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filepath = self._combined_json_folder / Path(
            f"combined_analysis_result_{timestamp}.json"
        )
        output_file = output_filepath.open("w")
        json.dump(combined_json, output_file, indent=4)

        if old_combined_json:
            os.remove(old_combined_json)

    def load_combined_json(self) -> dict:
        contents = os.listdir(self._combined_json_folder)
        if len(contents) > 1:
            logger.debug("loading the combined json object")
            old_combined_json: Path = self._combined_json_folder / Path(contents[0])
            return json.load(old_combined_json.open("r"))
        return {}
