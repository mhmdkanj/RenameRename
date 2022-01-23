from collections.abc import MutableMapping

class FileTransformation(MutableMapping):
    def __init__(self, filenames):
        self.transformations = {name: name for name in filenames}

    def __setitem__(self, key, value):
        self.transformations[key] = value

    def __getitem__(self, key):
        return self.transformations[key]

    def __delitem__(self, key):
        del self.transformations[key]

    def __iter__(self):
        return iter(self.transformations)

    def __len__(self):
        return len(self.transformations)

    def __str__(self):
        output = ''
        for k, v in self.transformations.items():
            output += k + " ----> " + v + "\n"
        return output

    def __repr__(self):
        return f"FileTransformation({repr(self.transformations)})"
