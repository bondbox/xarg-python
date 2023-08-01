#!/usr/bin/python3
# coding:utf-8

from argparse import Namespace
from errno import EINTR
from errno import ENOENT
import sys
from typing import Optional
from typing import Sequence
from typing import TextIO
from typing import Tuple

from .logger import level
from .parser import argp


def singleton(cls):
    instance = {}

    def _singleton_wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return _singleton_wrapper


@singleton
class commands:

    def __init__(self, *args, **kwargs):
        self.root: Optional[add_command] = None
        self.args: Optional[Namespace] = None

    @property
    def debug(self) -> int:
        if not isinstance(self.args, Namespace):
            return level.WARN

        if hasattr(self.args, "debug") and isinstance(self.args.debug, str):
            for name, member in level.__members__.items():
                if self.args.debug == name.lower():
                    return member

        return level.INFO

    def log(self, context: str, level: int = level.DEBUG):
        if level > self.debug:
            return

        std: TextIO = sys.stderr
        std.write(f"{context}\n")
        std.flush()

    def __add_optional_debug(self, argp: argp, root):
        if not isinstance(root, add_command):
            return

        options = argp.filter_optional_name('-d', '--debug')
        if len(options) <= 0:
            return

        def get_debug_level_name():
            return [key.lower() for key in level.__members__.keys()]

        argp.add_argument(*options,
                          type=int,
                          nargs="?",
                          const=level.DEBUG.name.lower(),
                          default=level.INFO.name.lower(),
                          choices=get_debug_level_name(),
                          help="specify log level, default info")

    def __add_parser(self, argp: argp, root):
        if not isinstance(root, add_command):
            return

        root.func(argp)
        self.__add_optional_debug(argp, root)

        subs = root.subs
        if not (isinstance(subs, list) or isinstance(subs, tuple)):
            return

        _sub = argp.add_subparsers(dest=root.sub_dest)
        for sub in subs:
            if not isinstance(sub, add_command):
                continue
            _arg = _sub.add_parser(sub.name, **sub.options)
            self.__add_parser(_arg, sub)

    def parse(self,
              argv: Optional[Sequence[str]] = None,
              **kwargs) -> Namespace:
        _arg = argp(**kwargs)
        self.__add_parser(_arg, self.root)
        args = _arg.parse_args(argv)

        self.args = args
        return self.args

    def __run(self, args, root) -> int:
        if not isinstance(root, add_command):
            return ENOENT

        if not isinstance(root.bind, run_command):
            return ENOENT

        ret = root.bind.func(args)
        if ret != 0 and ret is not None:
            return ret

        if hasattr(args, root.sub_dest):
            sub_name = getattr(args, root.sub_dest)

            subs = root.subs
            if not (isinstance(subs, list) or isinstance(subs, tuple)):
                return ENOENT

            for sub in subs:
                if not isinstance(sub, add_command):
                    continue

                if sub.name == sub_name:
                    return self.__run(args, sub)

            return ENOENT

        return 0

    def run(self, argv: Optional[Sequence[str]] = None, **kwargs) -> int:
        args = self.parse(argv, **kwargs)
        self.log(f"{args}", level.DEBUG)

        try:
            return self.__run(args, self.root)
        except KeyboardInterrupt:
            return EINTR
        except BaseException as e:
            self.log(f"{e}", level.FATAL)
            if self.debug >= level.DEBUG:
                raise e
            return 10000


class add_command:

    def __init__(self, name: str, **kwargs):
        self.cmds: commands = commands()
        self.name: str = name
        self.options = kwargs
        self.bind: Optional[run_command] = None
        self.subs: Optional[Tuple[add_command]] = None

    def __call__(self, cmd_func):
        self.func = cmd_func
        return self

    @property
    def sub_dest(self):
        return f"__sub_{self.name}_dest__"


class run_command:

    def __init__(self, cmd_bind: add_command, *subs):
        assert isinstance(cmd_bind, add_command)
        for sub in subs:
            assert isinstance(sub, add_command)

        cmd_bind.bind = self
        cmd_bind.subs = subs
        self.bind: add_command = cmd_bind
        commands().root = cmd_bind

    def __call__(self, run_func):
        self.func = run_func
        return self
