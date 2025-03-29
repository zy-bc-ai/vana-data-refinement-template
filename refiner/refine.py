import json
import logging
import os

from refiner.models.schema import Schema
from refiner.transformer.user_transformer import UserTransformer
from refiner.config import settings
from refiner.utils.ipfs import upload_json_to_ipfs

class Refiner:
    def __init__(self):
        self.db_path = os.path.join(settings.OUTPUT_DIR, 'db.libsql')

    def transform(self) -> None:
        """Transform all input files into the database."""
        logging.info("Starting data transformation")

        # Iterate through files and transform data
        for input_filename in os.listdir(settings.INPUT_DIR):
            input_file = os.path.join(settings.INPUT_DIR, input_filename)
            if os.path.splitext(input_file)[1].lower() == '.json':
                with open(input_file, 'r') as f:
                    input_data = json.load(f)

                    if input_filename == 'user.json':
                        # Transform account data
                        transformer = UserTransformer(self.db_path)
                        transformer.process(input_data)
                        logging.info(f"Transformed {input_filename}")
                        
                        # Create a schema file
                        schema_file = os.path.join(settings.OUTPUT_DIR, 'schema.json')
                        with open(schema_file, 'w') as f:
                            schema = Schema(
                                name=settings.SCHEMA_NAME,
                                version=settings.SCHEMA_VERSION,
                                description=settings.SCHEMA_DESCRIPTION,
                                dialect=settings.SCHEMA_DIALECT,
                                schema=transformer.get_schema()
                            )
                            json.dump(schema.model_dump(), f, indent=4)
                            logging.info(f"Schema saved to {schema_file}")
                            # ipfs_hash = upload_json_to_ipfs(schema.model_dump())
                            # logging.info(f"Schema uploaded to IPFS with hash: {ipfs_hash}")
                        continue

        logging.info("Data transformation completed successfully")
