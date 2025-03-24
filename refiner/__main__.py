import json
import logging
import os
import sys
import traceback
import zipfile
from typing import Dict, Any

from refiner.refine import Refiner

INPUT_DIR, OUTPUT_DIR = '/input', '/output'

logging.basicConfig(level=logging.INFO, format='%(message)s')


def load_config() -> Dict[str, Any]:
    """Load refinement configuration from environment variables."""
    config = {
        'input_dir': INPUT_DIR,
        'output_dir': OUTPUT_DIR,
    }
    logging.info(f"Using config: {json.dumps(config, indent=2)}")
    return config


def run() -> None:
    """Transform all input files into the database."""
    config = load_config()
    input_files_exist = os.path.isdir(INPUT_DIR) and bool(os.listdir(INPUT_DIR))

    if not input_files_exist:
        raise FileNotFoundError(f"No input files found in {INPUT_DIR}")
    extract_input()

    refiner = Refiner(config)
    refiner.transform()
    
    logging.info("Data transformation complete")


def extract_input() -> None:
    """
    If the input directory contains any zip files, extract them
    :return:
    """
    for input_filename in os.listdir(INPUT_DIR):
        input_file = os.path.join(INPUT_DIR, input_filename)

        if zipfile.is_zipfile(input_file):
            with zipfile.ZipFile(input_file, 'r') as zip_ref:
                zip_ref.extractall(INPUT_DIR)


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logging.error(f"Error during data transformation: {e}")
        traceback.print_exc()
        sys.exit(1)
