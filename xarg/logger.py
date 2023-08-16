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
    THREAD = 1 << 1
    FRAME = 1 << 2
    ALL = TIMESTAMP | THREAD | FRAME


TIMESTAMP = detail.TIMESTAMP
THREAD = detail.THREAD
FRAME = detail.FRAME
