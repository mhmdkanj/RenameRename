import os
import pytest
from pytest_mock import mocker
from renamerename.executor.executor import RenameExecutor
from renamerename.handlers.filetransformation import FileTransformation


class RenameMock:
    def __init__(self):
        self.dirfiles = set(['aaa', 'bbb', 'ccc.py', 'ddd.tar.gz', 'eee.txt', 'fff', 'ggg'])

    def __call__(self, src, dst):
        self.dirfiles.remove(src)
        self.dirfiles.add(dst)

    def exists(self, name):
        return name in self.dirfiles

class TestRenameExecutor:

    @pytest.fixture
    def rename_executor(self):
        return RenameExecutor()

    
    @pytest.fixture
    def get_filenames(self):
        return ['aaa', 'bbb', 'ccc.py', 'ddd.tar.gz', 'eee.txt']


    @pytest.fixture
    def get_names(self, get_filenames):
        return get_filenames + ['fff', 'ggg']


    # TODO: mock FileTransformation
    def test_adjust_duplicates_none(self, rename_executor, get_filenames, get_names):
        filetransformation = FileTransformation(get_filenames)
        filetransformation['aaa'] = 'foo_aaa'
        filetransformation['bbb'] = 'foo_bbb'
        filetransformation['ccc.py'] = 'foo_ccc.py'
        filetransformation['ddd.tar.gz'] = 'foo_ddd.tar.gz'
        filetransformation['eee.txt'] = 'foo_eee.txt'
        assert not filetransformation.has_duplicates()
        actual_transformation = rename_executor.adjust_duplicates(get_names, filetransformation)
        assert actual_transformation == filetransformation
        assert not actual_transformation.has_duplicates()


    def test_adjust_duplicates_one(self, rename_executor, get_filenames, get_names):
        # duplicates are exclusively in filetransformation
        filetransformation = FileTransformation(get_filenames)
        filetransformation['aaa'] = 'dup'  # duplicate
        filetransformation['bbb'] = 'foo_bbb'
        filetransformation['ccc.py'] = 'foo_ccc.py'
        filetransformation['ddd.tar.gz'] = 'foo_ddd.tar.gz'
        filetransformation['eee.txt'] = 'dup' # duplicate
        assert filetransformation.has_duplicates()
        actual_transformation = rename_executor.adjust_duplicates(get_names, filetransformation)
        assert actual_transformation == {
            'aaa': 'dup (1)',
            'bbb': 'foo_bbb',
            'ccc.py': 'foo_ccc.py',
            'ddd.tar.gz': 'foo_ddd.tar.gz',
            'eee.txt': 'dup (2)'
        }

    
    def test_adjust_duplicates_two(self, rename_executor, get_filenames, get_names):
        # duplicates reside in names and filetransformation
        filetransformation = FileTransformation(get_filenames)
        filetransformation['aaa'] = 'fff'  # duplicate with entry in names
        filetransformation['bbb'] = 'foo_bbb'
        filetransformation['ccc.py'] = 'foo_ccc.py'
        filetransformation['ddd.tar.gz'] = 'foo_ddd.tar.gz'
        filetransformation['eee.txt'] = 'foo_eee.txt'
        assert not filetransformation.has_duplicates()
        actual_transformation = rename_executor.adjust_duplicates(get_names, filetransformation)
        assert actual_transformation == {
            'aaa': 'fff (1)',
            'bbb': 'foo_bbb',
            'ccc.py': 'foo_ccc.py',
            'ddd.tar.gz': 'foo_ddd.tar.gz',
            'eee.txt': 'foo_eee.txt'
        }


    def test_execute(self, rename_executor, get_filenames, mocker):
        mocked_filesys = mocker.patch('os.rename', new_callable=RenameMock)
        mocker.patch('os.path.exists', mocked_filesys.exists)
        
        filetransformation = FileTransformation(get_filenames)
        filetransformation['aaa'] = 'fff' # duplicate with file in filesystem
        filetransformation['bbb'] = 'foo_bbb' 
        filetransformation['ccc.py'] = 'foo_ccc.py'
        filetransformation['ddd.tar.gz'] = 'foo_ddd'  # duplicate with below
        filetransformation['eee.txt'] = 'foo_ddd'  # duplicate with above
        
        rename_executor.execute(mocked_filesys.dirfiles, filetransformation)
        assert mocked_filesys.dirfiles == set(['fff (1)', 'foo_bbb', 'foo_ccc.py', 'foo_ddd (1)', 'foo_ddd (2)', 'fff', 'ggg'])
        mocker.resetall()