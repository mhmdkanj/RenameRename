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
            # TODO: check if file k exists
            if not os.path.exists(os.path.join(self.directory, v)):
                os.rename(os.path.join(self.directory, k), os.path.join(self.directory, v))
            else:
                self.actual_transformation = FileTransformation(dict(itertools.islice(filetransformation.items(), i)))
                if self.is_renaming_saved:
                    TransformationEncoder.save_transformation_to_json(self.directory, self.actual_transformation)

                raise FileExistsError(f"The file {os.path.join(self.directory, v)} already exists.")
        
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

