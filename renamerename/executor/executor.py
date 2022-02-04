import itertools
import logging
import os
from renamerename.handlers.handlers import FilenameHandler, FileTransformation
from renamerename.executor.encoder_decoder import TransformationEncoder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
) 

class RenameExecutor:

    def __init__(self, directory, save_renaming=False):
        self.directory = directory
        self.is_renaming_saved = save_renaming
        self.actual_transformation = None

    def execute(self, names, filetransformation):
        filetransformation = self.adjust_duplicates(names, filetransformation)

        for i, (k, v) in enumerate(filetransformation.items()):
            source_file_path = os.path.join(self.directory, k)
            target_file_path = os.path.join(self.directory, v)
            source_filename_exists = os.path.exists(source_file_path)
            target_filename_exists = os.path.exists(target_file_path)
            if not source_filename_exists or target_filename_exists:
                self.actual_transformation = FileTransformation(dict(itertools.islice(filetransformation.items(), i)))
                if self.is_renaming_saved:
                    TransformationEncoder.save_transformation_to_json(self.directory, self.actual_transformation)
                if not source_filename_exists:
                    raise FileNotFoundError(f"The source filename {source_file_path} does not exist.")
                if target_filename_exists:
                    raise FileExistsError(f"The target filename {target_file_path} already exists.")
            else:
                os.rename(source_file_path, target_file_path)
        
        if self.is_renaming_saved:
            TransformationEncoder.save_transformation_to_json(self.directory, filetransformation)

    
    def display_output(self, names, filetransformation):
        filetransformation = self.adjust_duplicates(names, filetransformation)
        print(filetransformation)
        

    def adjust_duplicates(self, names, filetransformation):
        # files not part of filter
        untouched_files = set(names) - set(filetransformation)
        
        # reverse the transformations dict
        reversed_transformations = filetransformation.get_reversed()

        for k, v in reversed_transformations.items():
            if len(v) > 1:
                # more than one filename is transformed to the same name
                for i, name in enumerate(v):
                    filetransformation[name] = FilenameHandler.add_suffix(filetransformation[name], f" ({str(i+1)})")
            elif len(v) == 1:
                # check if a transformed filename and an unfiltered file are duplicates
                if k in untouched_files:
                    filetransformation[next(iter(v))] = FilenameHandler.add_suffix(filetransformation[next(iter(v))], f" (1)")

        return filetransformation  


    @property
    def actual_transformation(self):
        return self._actual_transformation


    @actual_transformation.setter
    def actual_transformation(self, val):
        self._actual_transformation = val

