import pytest
from renamerename.handlers.handlers import DirectoryHandler, FilenameHandler
from renamerename.handlers.filetransformation import FileTransformation

class TestDirectoryHandler:
    
    @pytest.fixture
    def directory_handler_basic(self):
        names = ['file.txt', 'file.py', 'archive.tar.gz']
        return DirectoryHandler(names)


    @pytest.fixture
    def directory_handler(self):
        names = ['aaa.png', 'bbb.txt', 'ccc.tar.gz', 'ddd.png', 
                'eee.txt', 'fff', 'ggg', 'hhh.png', 'iii.tar.zip', 'jjj.pnj']
        handler = DirectoryHandler(names)
        handler.filter_names(".png$")
        return handler


    def test_basic_init(self, directory_handler_basic):
        assert directory_handler_basic.names == ['file.txt', 'file.py', 'archive.tar.gz']
        assert directory_handler_basic.filenames == ['file.txt', 'file.py', 'archive.tar.gz']
        assert type(directory_handler_basic.filenamehandler) == FilenameHandler
        assert isinstance(directory_handler_basic.filetransformations, FileTransformation)


    def test_filter_by_none(self, directory_handler_basic):
        directory_handler_basic.filter_names(filter=None)
        assert directory_handler_basic.filenames == ['file.txt', 'file.py', 'archive.tar.gz']


    def test_filter_names(self, directory_handler_basic):
        directory_handler_basic.filter_names(filter="file*")
        assert directory_handler_basic.filenames == ['file.txt', 'file.py']

    
    def test_filtered_names(self, directory_handler):
        assert directory_handler.filenames == ['aaa.png', 'ddd.png', 'hhh.png']

    def test_add_prefix(self, directory_handler):
        directory_handler.add_prefix("foo_")
        assert directory_handler.filetransformations == {
            'aaa.png': 'foo_aaa.png',
            'ddd.png': 'foo_ddd.png',
            'hhh.png': 'foo_hhh.png'
        }

    def test_add_suffix(self, directory_handler):
        directory_handler.add_suffix("_bar")
        assert directory_handler.filetransformations == {
            'aaa.png': 'aaa_bar.png',
            'ddd.png': 'ddd_bar.png',
            'hhh.png': 'hhh_bar.png'
        }

    def test_change_extension(self, directory_handler):
        directory_handler.change_extension(".jpeg")
        assert directory_handler.filetransformations == {
            'aaa.png': 'aaa.jpeg',
            'ddd.png': 'ddd.jpeg',
            'hhh.png': 'hhh.jpeg'
        }     

    def test_add_numbering(self, directory_handler):
        directory_handler.add_numbering("me")
        assert directory_handler.filetransformations == {
            'aaa.png': 'me0.png',
            'ddd.png': 'me1.png',
            'hhh.png': 'me2.png'
        }
