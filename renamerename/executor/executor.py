import os
from renamerename.handlers.handlers import FilenameHandler

class RenameExecutor:

    def __init__(self, directory):
        self.directory = directory

    def execute(self, names, filetransformation):
        filetransformation = self.adjust_duplicates(names, filetransformation)
        for k, v in filetransformation.items():
            if not os.path.exists(os.path.join(self.directory, v)):
                os.rename(os.path.join(self.directory, k), os.path.join(self.directory, v))
            else:
                raise FileExistsError(f"The file {os.path.join(self.directory, v)} already exists.")

    
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

