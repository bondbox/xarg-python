#!/usr/bin/python3
# coding:utf-8

import enum


@enum.unique
class level(enum.IntEnum):
    FATAL = 1
    ERROR = 10
    WARN = 100
    INFO = 1000
    DEBUG = 10000
    TRACE = 20000


FATAL = level.FATAL
ERROR = level.ERROR
WARN = level.WARN
INFO = level.INFO
DEBUG = level.DEBUG
TRACE = level.TRACE
