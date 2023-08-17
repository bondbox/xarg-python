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


@enum.unique
class detail(enum.IntFlag):
    NONE = 0
    TIMESTAMP = 1 << 0
    THREADID = 1 << 1
    THREADNAME = 1 << 2
    THREAD = THREADID | THREADNAME
    FILENAME = 1 << 5
    FUNCTION = 1 << 6
    FRAME = FILENAME | FUNCTION
    ALL = TIMESTAMP | THREAD | FRAME


TIMESTAMP = detail.TIMESTAMP
THREADID = detail.THREADID
THREADNAME = detail.THREADNAME
FILENAME = detail.FILENAME
FUNCTION = detail.FUNCTION
