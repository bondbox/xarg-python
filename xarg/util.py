# coding=utf-8


import os
import shutil
from typing import List

from .attribute import __author__
from .attribute import __author_email__
from .attribute import __description__
from .attribute import __name__
from .attribute import __prog_complete__
from .attribute import __prog_name__
from .attribute import __url_bugs__
from .attribute import __url_code__
from .attribute import __url_docs__
from .attribute import __url_home__
from .attribute import __version__


def singleton(cls):
    instance = {}

    def _singleton_wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return _singleton_wrapper


@singleton
class chdir:
    '''Change directory
    '''

    def __init__(self):
        self.__stack: List[str] = []

    def pushd(self, path: str):
        '''Add directory to stack.
        '''
        assert isinstance(path, str), f"type '{type(path)}' is not str"
        assert os.path.isdir(path), f"path '{path}' is not directory"
        self.__stack.append(os.getcwd())
        os.chdir(path)

    def popd(self):
        '''Remove directory from stack.
        '''
        assert len(self.__stack) > 0
        os.chdir(self.__stack.pop())


class safile:
    '''Secure read and write files

    Backup before writing and restore (if backup exists) before reading.
    '''

    @classmethod
    def get_backup_path(cls, origin: str) -> str:
        '''Unified backup path
        '''
        return f"{origin}.bak"

    @classmethod
    def create_backup(cls, path: str) -> bool:
        '''Create a backup before writing file
        '''
        pbak: str = cls.get_backup_path(path)
        if os.path.isfile(pbak):  # Restore before creating a new backup
            assert cls.restore(path), f"restore '{path}' failed"
        assert not os.path.exists(pbak), f"backup file '{pbak}' already exists"
        if not os.path.exists(path):  # No need for backup
            return True
        assert os.path.isfile(path), f"'{path}' is not a regular file"
        assert shutil.move(src=path, dst=pbak) == pbak, \
            f"backup '{path}' failed"
        return os.path.exists(pbak)

    @classmethod
    def delete_backup(cls, path: str) -> bool:
        '''Delete backup after writing file
        '''
        pbak: str = cls.get_backup_path(path)
        if os.path.isfile(pbak):
            os.remove(pbak)
        return not os.path.exists(pbak)

    @classmethod
    def restore(cls, path: str) -> bool:
        '''Restore (if backup exists) before reading file
        '''
        pbak: str = cls.get_backup_path(path)
        if os.path.isfile(pbak):
            if os.path.isfile(path):
                os.remove(path)
            assert not os.path.exists(path), f"file '{path}' still exists"
            assert shutil.move(src=pbak, dst=path) == path, \
                f"restore backup file '{pbak}' to '{path}' failed"
        return not os.path.exists(pbak)
