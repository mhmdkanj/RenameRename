import json
import logging
import os
from datetime import datetime
from renamerename.handlers.filetransformation import FileTransformation

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

class TransformationEncoder:

    @staticmethod
    def encode_to_json_file(filetransformation, path):
        with open(path, 'w') as f:
            json.dump(filetransformation.transformations, f, sort_keys=True, indent=0)

    @staticmethod
    def save_transformation_to_json(directory, filetransformation):
        save_path = os.path.join(directory, "renaming_" + datetime.now().strftime("%d%m%Y_%H%M%S") + ".json")
        TransformationEncoder.encode_to_json_file(filetransformation, save_path)
        logging.info(f"Saved renaming to {save_path}") 


class TransformationDecoder:

    @staticmethod
    def decode_from_json_file(path):
        with open(path, 'r') as f:
            content = json.load(f)
        return FileTransformation(content)

