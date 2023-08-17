#!/usr/bin/python3
# coding:utf-8

from argparse import FileType
from argparse import Namespace
from datetime import datetime
from errno import EINTR
from errno import ENOENT
import os
import sys
from threading import current_thread
from typing import Optional
from typing import Sequence
from typing import TextIO
from typing import Tuple
from typing import Union

from .logger import FILENAME
from .logger import FUNCTION
from .logger import THREADID
from .logger import THREADNAME
from .logger import TIMESTAMP
from .logger import detail
from .logger import level
from .parser import argp


class add_command:
    '''
    Define command-line arguments.

    For example:

    from xarg import add_command\n
    from xarg import argp\n

    @add_command("example")\n
    def cmd(_arg: argp):\n
        argp.add_opt_on("-t", "--test")\n
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

    from xarg import argp\n
    from xarg import run_command\n

    @run_command(cmd, cmd_get, cmd_set)\n
    def run(cmds: commands) -> int:\n
        return 0\n
    '''

    def __init__(self, cmd_bind: add_command, *subs: add_command):
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

    from typing import Optional\n
    from typing import Sequence\n

    from xarg import add_command\n
    from xarg import argp\n
    from xarg import commands\n
    from xarg import run_command\n

    @add_command("example")\n
    def cmd(_arg: argp):\n
        argp.add_opt_on("-t", "--test")\n

    @run_command(cmd, cmd_get, cmd_set)\n
    def run(cmds: commands) -> int:\n
        return 0\n

    def main(argv: Optional[Sequence[str]] = None) -> int:\n
        return commands().run(\n
            root=cmd,\n
            argv=argv,\n
            prog="xarg-example",\n
            description="Simple command-line tool based on argparse.")\n
    '''

    def __init__(self):
        self.__args: Namespace = Namespace()
        self.__root: Optional[add_command] = None
        self.__version: Optional[str] = None
        self.__timefmt: Optional[str] = "%Y-%m-%d %a %H:%M:%S.%f"
        self.__log_details: detail = detail.NONE
        self.__debug_level: level = level.WARN

    @property
    def root(self) -> Optional[add_command]:
        '''
        Root Command.
        '''
        return self.__root

    @root.setter
    def root(self, value: add_command):
        if isinstance(value, add_command):
            self.__root = value

    @property
    def args(self) -> Namespace:
        '''
        Namespace after parse arguments.
        '''
        assert isinstance(self.__args, Namespace)
        return self.__args

    @args.setter
    def args(self, value: Namespace):
        if isinstance(value, Namespace):
            self.__args = value

    @property
    def version(self) -> Optional[str]:
        '''
        Custom version for "-v" or "--version" output.
        '''
        return self.__version

    @version.setter
    def version(self, value: str):
        if isinstance(value, str):
            _version = value.strip()
            self.__version = _version

    @property
    def debug_level(self) -> level:
        '''
        The logger output level. If not specified, the default is WARN.
        '''
        return self.__debug_level

    @debug_level.setter
    def debug_level(self, value: Union[level, str]):
        members = level.__members__
        if isinstance(value, str):
            key = value.upper()
            if key in members.keys():
                self.__debug_level = members[key]
        elif value in members.values():
            self.__debug_level = {v: v for v in members.values()}[value]

    @property
    def log_detail(self) -> detail:
        '''
        The logger output details. If not specified, the default is NONE.
        '''
        return self.__log_details

    @log_detail.setter
    def log_detail(self, value: detail):
        if isinstance(value, detail):
            self.__log_details = value

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
        if isinstance(value, str):
            _timefmt = value.strip()
            self.__timefmt = _timefmt
        elif value is None:
            self.__timefmt = value

    def stdout(self, context):
        '''
        Output string to sys.stdout.
        '''
        sys.stdout.write(f"{context}\n")
        sys.stdout.flush()

    def stderr(self, context):
        '''
        Output string to sys.stderr.
        '''
        sys.stderr.write(f"{context}\n")
        sys.stderr.flush()

    def log(self, context, level: level = level.DEBUG):
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
        if TIMESTAMP in self.log_detail and isinstance(self.timefmt, str):
            items.append(datetime.now().strftime(self.timefmt))
        if THREADID in self.log_detail:
            ident = current_thread().ident
            if isinstance(ident, int):
                items.append(str(ident))
        if THREADNAME in self.log_detail:
            items.append(current_thread().getName())
        if FILENAME in self.log_detail or FUNCTION in self.log_detail:
            f_back = sys._getframe().f_back
            if f_back:
                if FILENAME in self.log_detail:
                    filename = f_back.f_code.co_filename
                    lineno = f_back.f_lineno
                    items.append(f"{os.path.basename(filename)}:{lineno}")
                if FUNCTION in self.log_detail:
                    items.append(f_back.f_code.co_name)
        items.append(f"{context}\n")

        std.write(" ".join(items))
        std.flush()

    def __add_optional_version(self, argp: argp, root: add_command):
        if not isinstance(self.version, str):
            return

        if not isinstance(root, add_command):
            return

        options = argp.filter_optional_name("-v", "--version")
        if len(options) <= 0:
            return

        argp.add_argument(*options,
                          action="version",
                          version=f"%(prog)s {self.version}")

    def __add_optional_debug(self, argp: argp, root: add_command):
        if not isinstance(root, add_command):
            return

        options = argp.filter_optional_name("-d", "--debug")
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

    def __add_optional_output(self, argp: argp, root: add_command):
        if not isinstance(root, add_command):
            return

        options = argp.filter_optional_name("-o", "--output")
        if len(options) <= 0:
            return

        group = argp.argument_group("logger optional arguments")
        group.add_argument(*options,
                           type=FileType("a", encoding="UTF-8"),
                           nargs="?",
                           const=sys.stdout,
                           default=sys.stderr,
                           metavar="log file",
                           dest="_log_output_stream_",
                           help="Specify log output stream, default stderr.\n"
                           "If a file path is specified, output the log to\n"
                           "the specified file, otherwise redirect to stdout.")

    def __add_optional_detail(self, argp: argp, root: add_command):
        if not isinstance(root, add_command):
            return

        options = argp.filter_optional_name("--detail", "--log-detail")
        if len(options) <= 0:
            return

        if "--detail" in options:
            options -= set(["--log-detail"])

        def get_log_detail_name():
            values = set(detail.__members__.values()) - set([detail.NONE])
            return [v.name.lower() for v in values]

        group = argp.argument_group("logger optional arguments")
        group.add_argument(*options,
                           type=str,
                           nargs="+",
                           default=[],
                           choices=get_log_detail_name(),
                           dest="_log_detail_",
                           help="Specify log output details, default\n"
                           f"{detail.NONE.name.lower()}.\n")

    def __add_parser(self, argp: argp, root: add_command, **kwargs):
        if not isinstance(root, add_command):
            return

        root.func(argp)
        self.__add_optional_debug(argp, root)
        self.__add_optional_output(argp, root)
        self.__add_optional_detail(argp, root)

        subs = root.subs
        if not isinstance(subs, tuple) or len(subs) <= 0:
            return

        _sub = argp.add_subparsers(dest=root.sub_dest)
        for sub in subs:
            if not isinstance(sub, add_command):
                continue
            for key in kwargs:
                sub.options.setdefault(key, kwargs.get(key))
            _arg = _sub.add_parser(sub.name, **sub.options)
            self.__add_parser(_arg, sub)

    def parse(self,
              root: Optional[add_command] = None,
              argv: Optional[Sequence[str]] = None,
              **kwargs) -> Namespace:
        '''
        Parse the command line.
        '''
        if root is None:
            root = self.__root

        assert isinstance(root, add_command)

        _arg = argp(**kwargs)
        self.__add_parser(_arg, root, **kwargs)
        self.__add_optional_version(_arg, root)

        args = _arg.parse_args(argv)
        assert isinstance(args, Namespace)

        # save debug level to local variable
        if hasattr(args, "_debug_level_str_") and\
           isinstance(args._debug_level_str_, str):
            self.debug_level = args._debug_level_str_

        # save log detail to local variable
        if hasattr(args, "_log_detail_") and\
           isinstance(args._log_detail_, list):
            for v in args._log_detail_:
                assert isinstance(v, str)
                self.log_detail |= detail[v.upper()]

        self.__args = args
        return self.__args

    def __run(self, args: Namespace, root: add_command) -> int:
        if not isinstance(root, add_command):
            return ENOENT

        if not isinstance(root.bind, run_command):
            return ENOENT

        ret = root.bind.func(self)
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

    def run(self,
            root: Optional[add_command] = None,
            argv: Optional[Sequence[str]] = None,
            **kwargs) -> int:
        '''
        Parse and run the command line.
        '''
        if root is None:
            root = self.__root

        if not isinstance(root, add_command):
            self.log("cannot find root", level.DEBUG)
            return ENOENT

        args = self.parse(root, argv, **kwargs)
        self.log(f"{args}", level.DEBUG)

        try:
            version = self.version
            if isinstance(version, str):
                self.log(f"version: {version}", level.INFO)

            return self.__run(args, root)
        except KeyboardInterrupt:
            return EINTR
        except BaseException as e:
            self.log(f"{e}", level.FATAL)
            if self.debug_level >= level.DEBUG:
                raise e
            return 10000
