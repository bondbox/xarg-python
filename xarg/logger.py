# coding:utf-8

import logging
import os
import sys
from time import time
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from typing import TextIO

from colorlog import ColoredFormatter
from colorlog.formatter import LogColors

from .attribute import __prog_name__ as prog


class once_filter(logging.Filter):
    def __init__(self, name: str = "logging_once_filter",
                 max_interval_seconds: int = 60):
        self.__max_interval: int = max(3, max_interval_seconds)
        self.__timestamp: float = time()
        self.__message = None
        super().__init__(name)

    def filter(self, record: logging.LogRecord) -> bool:
        current_message = (record.msg, record.args)
        if current_message != self.__message or self.timeout:
            self.__message = current_message
            self.__timestamp = time()
            return True
        return False

    @property
    def max_interval_seconds(self) -> int:
        return self.__max_interval

    @property
    def interval_seconds(self) -> float:
        return time() - self.__timestamp

    @property
    def timeout(self) -> bool:
        return self.interval_seconds > self.max_interval_seconds


class log:
    LOG_LEVEL_FATAL: str = "FATAL"
    LOG_LEVEL_ERROR: str = "ERROR"
    LOG_LEVEL_WARN: str = "WARN"
    LOG_LEVEL_INFO: str = "INFO"
    LOG_LEVEL_DEBUG: str = "DEBUG"
    DEFAULT_LOG_FORMAT: str = "%(log_color)s%(message)s"
    DEFAULT_LOG_COLORS: LogColors = {
        LOG_LEVEL_FATAL: "light_red",
        LOG_LEVEL_ERROR: "red",
        LOG_LEVEL_WARN: "yellow",
        LOG_LEVEL_INFO: "white",
        LOG_LEVEL_DEBUG: "black",
    }
    ALLOWED_LOG_LEVELS: List[str] = [
        k.lower() for k in DEFAULT_LOG_COLORS.keys()
    ]

    def __init__(self):
        self.__initiated_names: Set[str] = set()

    def logger_initiated(self, name: str) -> bool:
        return name in self.__initiated_names

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        return logging.getLogger(name if isinstance(name, str) else prog)

    def initiate_logger(self, logger: logging.Logger,
                        level: Optional[str] = None,
                        handlers: Optional[Iterable[logging.Handler]] = None,
                        filters: Optional[Iterable[logging.Filter]] = None):
        assert not self.logger_initiated(logger.name)

        if isinstance(level, str):
            logger.setLevel(logging._nameToLevel[level.upper()])

        if filters is None:
            filters = [once_filter()]

        for filter in filters:
            logger.addFilter(filter)

        if handlers is None:
            handlers = [self.new_stream_handler(stream=sys.stdout)]

        for handler in handlers:
            logger.addHandler(handler)

        self.__initiated_names.add(logger.name)

    @classmethod
    def new_stream_handler(cls, stream: Optional[TextIO] = None,
                           fmt: Optional[str] = None,
                           log_colors: Optional[LogColors] = None
                           ) -> logging.StreamHandler:
        if fmt is None:
            fmt = cls.DEFAULT_LOG_FORMAT
        if log_colors is None:
            log_colors = cls.DEFAULT_LOG_COLORS
        formatter: logging.Formatter = ColoredFormatter(
            fmt=fmt, datefmt=None, log_colors=log_colors)
        handler: logging.StreamHandler = logging.StreamHandler(stream=stream)
        handler.setFormatter(formatter)
        return handler

    @classmethod
    def new_file_handler(cls, filename: str,
                         fmt: Optional[str] = None) -> logging.FileHandler:
        assert isinstance(filename, str), f"Unexpected type: {type(filename)}"
        dirname: str = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        assert os.path.isdir(dirname), f"{dirname} not an existing directory"
        formatter: logging.Formatter = ColoredFormatter(
            fmt=fmt, datefmt=None, no_color=True)
        handler: logging.FileHandler = logging.FileHandler(filename=filename)
        handler.setFormatter(formatter)
        return handler
