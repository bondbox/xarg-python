# coding=utf-8

import os
import shutil


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
    def create_backup(cls, path: str, copy: bool = False) -> bool:
        '''Create a backup before writing file

        Backup files with '.bak' suffix will be created in the same directory.
        By default shutil.move() is used to create the backup file, which will
        use os.rename() to rename the original file. This will make the backup
        very efficient.
        But, if you wish to append to the original file, you need to specify
        'copy=True' to use shutil.copy2().
        '''
        pbak: str = cls.get_backup_path(path)
        if os.path.isfile(pbak):  # Restore before creating a new backup
            assert cls.restore(path), f"restore '{path}' failed"
        assert not os.path.exists(pbak), f"backup file '{pbak}' already exists"
        if not os.path.exists(path):  # No need for backup
            return True
        assert os.path.isfile(path), f"'{path}' is not a regular file"
        method = shutil.copy2 if copy else shutil.move
        assert method(src=path, dst=pbak) == pbak, f"backup '{path}' failed"
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
