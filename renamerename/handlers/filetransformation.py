from collections.abc import MutableMapping

class FileTransformation(MutableMapping):
    def __init__(self, transformations: dict):
        if type(transformations) == dict:
            self.transformations = transformations
        else:
            raise TypeError("An object type other than dict was passed to FileTransformation constructor.")


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
        return f"{self.__class__.__name__}({repr(self.transformations)})"

    
    @classmethod
    def from_list(cls, filenames):
        return cls({name: name for name in filenames})


    def get_reversed(self):
        reversed_transformations = {}
        for k, v in self.transformations.items():
            reversed_transformations.setdefault(v, []).append(k)
        return reversed_transformations


    def has_duplicates(self):
        for v in self.get_reversed().values():
            if len(v) > 1:
                return True
        return False
