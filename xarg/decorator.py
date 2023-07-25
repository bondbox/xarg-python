#!/usr/bin/python3
# coding:utf-8

from errno import EINTR
from errno import ENOENT
import sys
from typing import List
from typing import Optional
from typing import Tuple

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

    def __add_parser(self, argp: argp, root):
        if not isinstance(root, add_command):
            return

        root.func(argp)

        subs = root.subs
        if not (isinstance(subs, list) or isinstance(subs, tuple)):
            return

        _sub = argp.add_subparsers(dest=root.sub_dest)
        for sub in subs:
            if not isinstance(sub, add_command):
                continue
            _arg = _sub.add_parser(sub.name, **sub.options)
            self.__add_parser(_arg, sub)

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

    def run(self, argv: Optional[List[str]] = None, **kwargs) -> int:
        _arg = argp(**kwargs)
        self.__add_parser(_arg, self.root)
        args = _arg.parse_args(argv)

        if hasattr(args, "debug") and args.debug:
            sys.stderr.write(f"{args}\n")
            sys.stderr.flush()

        try:
            return self.__run(args, self.root)
        except KeyboardInterrupt:
            return EINTR
        except BaseException as e:
            if hasattr(args, "debug") and args.debug:
                raise e
            sys.stderr.write(f"{e}\n")
            sys.stderr.flush()
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
