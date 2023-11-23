#!/usr/bin/python3
# coding=utf-8

__package_name__ = "xarg-python"
__prog_name__ = "xarg"
__prog_complete__ = "xargcomplete"
__version__ = "0.11.beta.2"

URL_PROG = "https://github.com/bondbox/xarg-python"


def singleton(cls):
    instance = {}

    def _singleton_wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return _singleton_wrapper
