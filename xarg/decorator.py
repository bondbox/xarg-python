#!/usr/bin/python3
# coding:utf-8

from argparse import Namespace
from argparse import FileType
from datetime import datetime
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
    '''
    Singleton command-line tool based on argparse.

    Define and bind callback functions before calling run() or parse().

    For example:

    @add_command('example')\n
    def cmd(argp: argp):\n
        argp.add_opt_on('-t', '--test')\n

    @run_command(cmd, cmd_get, cmd_set)\n
    def run(args) -> int:\n
        return 0\n

    def main(argv: Optional[List[str]] = None) -> int:\n
        return commands().run(\n
            prog="xarg-example",\n
            description="Simple command-line tool based on argparse.")\n
    '''

    def __init__(self, *args, **kwargs):
        self.root: Optional[add_command] = None
        self.args: Optional[Namespace] = None
        self.__timefmt: Optional[str] = "%Y-%m-%d %a %H:%M:%S.%f"

    @property
    def timefmt(self) -> Optional[str]:
        '''
        The timestamp format for the logger.

        Suggestion: only set before running! If the log format is changed
        while calling run(), the output will be messy.
        '''
        return self.__timefmt

    @timefmt.setter
    def timefmt(self, value: Optional[str]):
        self.__timefmt = value

    @property
    def debug_level(self) -> int:
        '''
        The logger output level. If not specified, the default is WARN.
        '''
        if isinstance(self.args, Namespace) and\
           hasattr(self.args, "_debug_level_str_") and\
           isinstance(self.args._debug_level_str_, str):
            return level.__members__[self.args._debug_level_str_.upper()]

        return level.WARN

    def log(self, context, level: int = level.DEBUG):
        '''
        Output logs to the specified stream.

        Each log should define the level or use the default. Only when
        the log level is less than or equal to the specified level, the
        log will be output to the specified stream.
        '''
        if level > self.debug_level:
            return

        std: TextIO = sys.stderr
        if isinstance(self.args, Namespace) and\
           hasattr(self.args, "_log_output_stream_"):
            std = self.args._log_output_stream_

        items = []
        if isinstance(self.timefmt, str):
            items.append(datetime.now().strftime(self.timefmt))
        items.append(f'{context}\n')
        std.write(" ".join(items))
        std.flush()

    def __add_optional_debug(self, argp: argp, root):
        if not isinstance(root, add_command):
            return

        options = argp.filter_optional_name('-d', '--debug')
        if len(options) <= 0:
            return

        def get_debug_level_name():
            return [key.lower() for key in level.__members__.keys()]

        group = argp.argument_group("logger optional arguments")
        group.add_argument(*options,
                           type=str,
                           nargs="?",
                           const=level.DEBUG.name.lower(),
                           default=level.INFO.name.lower(),
                           choices=get_debug_level_name(),
                           dest="_debug_level_str_",
                           help="Specify log level, default\n"
                           f"{level.INFO.name.lower()}.\n"
                           "If this option has no value, it means\n"
                           f"{level.DEBUG.name.lower()}.\n")

    def __add_optional_output(self, argp: argp, root):
        if not isinstance(root, add_command):
            return

        options = argp.filter_optional_name('-o', '--output')
        if len(options) <= 0:
            return

        group = argp.argument_group("logger optional arguments")
        group.add_argument(*options,
                           type=FileType('a', encoding='UTF-8'),
                           nargs="?",
                           const=sys.stdout,
                           default=sys.stderr,
                           metavar='log output file',
                           dest="_log_output_stream_",
                           help="Specify log output stream, default stderr.\n"
                           "If a file path is specified, output the log to\n"
                           "the specified file, otherwise redirect to stdout.")

    def __add_parser(self, argp: argp, root):
        if not isinstance(root, add_command):
            return

        root.func(argp)
        self.__add_optional_debug(argp, root)
        self.__add_optional_output(argp, root)

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
        '''
        Parse the command line.
        '''
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
        '''
        Parse and run the command line.
        '''
        args = self.parse(argv, **kwargs)
        self.log(f"{args}", level.DEBUG)

        try:
            return self.__run(args, self.root)
        except KeyboardInterrupt:
            return EINTR
        except BaseException as e:
            self.log(f"{e}", level.FATAL)
            if self.debug_level >= level.DEBUG:
                raise e
            return 10000


class add_command:
    '''
    Define command-line arguments.

    For example:

    @add_command('example')\n
    def cmd(argp: argp):\n
        argp.add_opt_on('-t', '--test')\n
    '''

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
    '''
    Bind command-line arguments and subcommands, define callback functions.

    For example:

    @run_command(cmd, cmd_get, cmd_set)\n
    def run(args) -> int:\n
        return 0\n
    '''

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
