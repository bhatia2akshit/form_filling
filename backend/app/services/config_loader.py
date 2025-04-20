import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_config(file_path):
    config = {}
    try:
        if Path(file_path).exists():
            f = Path(file_path).open("r")
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    config[key.strip()] = value.strip()
            f.close()
        if config['AZURE_ENDPOINT'] == "<>" or config['AZURE_KEY'] == "<>" or config['AZURE_LLM_ENDPOINT'] == "<>" or config['AZURE_LLM_KEY'] == "<>":
            raise ValueError("Azure credentials are not set in the config file.")

    except FileNotFoundError as file_error:
        logger.error(f"Configuration file not found: {file_error}")

    logger.info(f"Loaded configuration: {config}")
    return config


config = load_config("./config.txt")
