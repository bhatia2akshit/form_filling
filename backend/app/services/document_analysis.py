from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import os
from azure.core.credentials import AzureKeyCredential
import json
from datetime import datetime
from pathlib import Path


class DocumentAnalysisService:
    
    def __init__(self, config):
        self._combined_json_path: Path = Path(config["COMBINED_JSON_FOLDER"])
        self._json_folder: Path = Path(config["JSON_FOLDER"])
        self._azure_endpoint: str = config["AZURE_ENDPOINT"]
        self._azure_key: str = config["AZURE_KEY"]

    def analyze_document(self, file_path) -> dict:
        try:
            document_analysis_client = DocumentAnalysisClient(
                endpoint=self._azure_endpoint,
                credential=AzureKeyCredential(self._azure_key),
            )

            file_opened = Path(file_path).open("rb")

            poller = document_analysis_client.begin_analyze_document(
                "prebuilt-document", file_opened
            )
            result = poller.result()
            print("result is prepared")

            formatted_result = {}
            for kv_pair in result.key_value_pairs:
                if kv_pair.key and kv_pair.value:
                    formatted_result[kv_pair.key.content] = [kv_pair.value.content]
                else:
                    formatted_result[kv_pair.key.content] = [kv_pair.key.content]

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename: Path = Path(f"analysis_result_{timestamp}.json")
            output_path: Path = self._json_folder / output_filename

            output_file = output_path.open("w")
            json.dump(formatted_result, output_file, indent=4)

            print(f"Saved analysis to {output_path}")

            return formatted_result
        except Exception as e:
            current_app.logger.error(f"Error analyzing document: {str(e)}")
            raise

    def summarize_jsons(self):
        """Summarizes the json objects available in the json folder and make a unified json object"""

        # check if there is already an existing json object.
        contents = os.listdir(self._combined_json_path)

        if len(contents) > 1:
            combined_json: {} = json.load(
                (self._combined_json_path / Path(contents[0])).open("r")
            )
        else:
            combined_json: {} = {}

        # For same fields, make an array of values.

        # load the json files collected in json objects
        json_files = os.listdir(self._json_folder)
        for file in json_files:
            if file.endswith(".json"):
                json_file = json.load((self._json_folder / Path(file)).open("r"))
                for key, value in json_file.items():
                    # if the key is already present in the combined json object, append the value to the existing value
                    if key in combined_json:
                        if isinstance(value, list):
                            combined_json[key].extend(value)
                        else:
                            combined_json[key] = [combined_json[key], value]
                    else:
                        combined_json[key] = [value]

        # save combined_json to the folder.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filepath = Path(f"combined_analysis_result_{timestamp}.json")
        output_file = output_filepath.open("w")
        json.dump(combined_json, output_file, indent=4)
