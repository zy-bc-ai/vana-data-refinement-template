import json
import logging
import os
from typing import Dict, Any

from refiner.transformer.user_transformer import UserTransformer

class Refiner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_path = os.path.join(config['output_dir'], 'db.libsql')

    def transform(self) -> None:
        """Transform all input files into the database."""
        logging.info("Starting data transformation")

        # Iterate through files and transform data
        for input_filename in os.listdir(self.config['input_dir']):
            input_file = os.path.join(self.config['input_dir'], input_filename)
            if os.path.splitext(input_file)[1].lower() == '.json':
                with open(input_file, 'r') as f:
                    input_data = json.load(f)

                    if input_filename == 'user.json':
                        # Transform account data
                        transformer = UserTransformer(self.db_path)
                        transformer.process(input_data)
                        logging.info(f"Transformed {input_filename}")
                        logging.info(f"Schema {transformer.get_schema()}")
                        continue

        logging.info("Data transformation completed successfully")
