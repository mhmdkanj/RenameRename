import pytest
from renamerename.handlers.filetransformation import FileTransformation

class TestFileTransformation:

    @pytest.fixture
    def file_transformation_basic(self):
        names = ['one.py', 'two.txt', 'three.tar.gz']
        return FileTransformation(names)


    @pytest.fixture
    def file_transformation(self):
        names = ['one.py', 'two.txt', 'three.tar.gz']
        t = FileTransformation(names)
        t['one.py'] = 'foo_one.py'
        t['two.txt'] = 'two_bar.txt'
        t['three.tar.gz'] = 'three.zip'
        return t


    @pytest.fixture
    def file_transformation_with_duplicates(self):
        names = ['file.py', 'file.txt', 'three.tar.gz', 'three', 'something']
        t = FileTransformation(names)
        t['file.py'] = 'file'
        t['file.txt'] = 'file'
        t['three.tar.gz'] = 'three.zip'
        t['three'] = 'three.zip'
        t['something'] = 'foo'
        return t


    def test_init(self, file_transformation_basic):
        assert file_transformation_basic.transformations == {
            'one.py': 'one.py',
            'two.txt': 'two.txt',
            'three.tar.gz': 'three.tar.gz'
        }


    def test_get_set_item(self, file_transformation_basic):
        assert file_transformation_basic['one.py'] == 'one.py'
        file_transformation_basic['one.py'] = 'something_else'
        assert file_transformation_basic['one.py'] == 'something_else'


    def test_str_output(self, file_transformation):
        expected_str = "one.py ----> foo_one.py\n"\
                       "two.txt ----> two_bar.txt\n"\
                       "three.tar.gz ----> three.zip\n"
        assert str(file_transformation) == expected_str


    def test_get_reversed(self, file_transformation):
        assert file_transformation.get_reversed() == {
            'foo_one.py': ['one.py'],
            'two_bar.txt': ['two.txt'],
            'three.zip': ['three.tar.gz']
        }


    def test_get_reversed_with_duplicates(self, file_transformation_with_duplicates):
        assert file_transformation_with_duplicates.get_reversed() == {
            'file': ['file.py', 'file.txt'],
            'three.zip': ['three.tar.gz', 'three'],
            'foo': ['something']
        }


    def test_has_no_duplicates(self, file_transformation):
        assert not file_transformation.has_duplicates()


    def test_has_duplicates(self, file_transformation_with_duplicates):
        assert file_transformation_with_duplicates.has_duplicates()