#!/usr/bin/python3
# coding=utf-8


import os
from typing import List

__package_name__ = "xarg-python"
__prog_name__ = "xarg"
__prog_complete__ = "xargcomplete"
__version__ = "1.1.beta.1"

URL_PROG = "https://github.com/bondbox/xarg-python"


def singleton(cls):
    instance = {}

    def _singleton_wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return _singleton_wrapper


@singleton
class chdir:
    '''
    Change directory
    '''

    def __init__(self):
        self.__stack: List[str] = []

    def __del__(self):
        if len(self.__stack) > 0:
            os.chdir(self.__stack[0])

    def pushd(self, path: str):
        '''
        Add directory to stack.
        '''
        assert isinstance(path, str)
        assert os.path.isdir(path)
        self.__stack.append(os.getcwd())
        os.chdir(path)

    def popd(self):
        '''
        Remove directory from stack.
        '''
        assert len(self.__stack) > 0
        os.chdir(self.__stack.pop())
