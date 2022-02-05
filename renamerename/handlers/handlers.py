import fnmatch
from pathlib import Path
from renamerename.handlers.filetransformation import FileTransformation 


class FilenameHandler:

    @staticmethod
    def add_prefix(name, prefix):
        return prefix + name
    

    @staticmethod
    def add_suffix(name, suffix):
        filename, ext = FilenameHandler.get_components(name)
        return filename + suffix + ext


    @staticmethod
    def change_extension(name, new_ext):
        filename, _ = FilenameHandler.get_components(name)
        return filename + new_ext

    
    @staticmethod
    def change_name(name, new_filename):
        _, ext = FilenameHandler.get_components(name)
        return new_filename + ext 
    

    @staticmethod
    def get_components(name):
        extensions = Path(name).suffixes
        filename = Path(name)
        for i, _ in enumerate(extensions):
            filename = Path(filename.stem)
        return str(filename), ''.join(extensions)


class FileListHandler:
    
    def __init__(self, names):
        self.names = names
        self.filenames = self.names
        self.filenamehandler = FilenameHandler()
        self.filetransformations = FileTransformation.from_list(self.filenames)


    def filter_names(self, filter=None):
        if filter is None:
            self.filenames = self.names
        else:
            self.filenames = fnmatch.filter(self.names, filter)

    
    def add_prefix(self, prefix):
        for name in self.filenames:
            self.filetransformations[name] = self.filenamehandler.add_prefix(self.filetransformations[name], prefix)


    def add_suffix(self, suffix):
        for name in self.filenames:
            self.filetransformations[name] = self.filenamehandler.add_suffix(self.filetransformations[name], suffix)


    def change_extension(self, new_ext):
        for name in self.filenames:
            self.filetransformations[name] = self.filenamehandler.change_extension(self.filetransformations[name], new_ext)

    
    def add_numbering(self, prefix):
        for i, name in enumerate(self.filenames):
            new_name = self.filenamehandler.change_name(self.filetransformations[name], prefix)
            self.filetransformations[name] = self.filenamehandler.add_suffix(new_name, str(i))


    @property
    def filetransformations(self):
        return self._filetransformations


    @filetransformations.setter
    def filetransformations(self, val):
        self._filetransformations = val

    @property
    def filenames(self):
        return self._filenames

    @filenames.setter
    def filenames(self, val):
        self._filenames = val
        self.filetransformations = FileTransformation.from_list(self._filenames)
