#!/usr/bin/python3
# coding:utf-8

from argparse import Namespace
from errno import EINTR
from errno import ENOENT
import logging
import sys
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from argcomplete import autocomplete

from .parser import argp
from .util import singleton


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
        if "help" in kwargs and "description" not in kwargs:
            kwargs["description"] = kwargs["help"]
        if "description" in kwargs and "help" not in kwargs:
            kwargs["help"] = kwargs["description"]
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
        self.__prog: str = "xarg"
        self.__root: Optional[add_command] = None
        self.__args: Namespace = Namespace()
        self.__version: Optional[str] = None

    @property
    def prog(self) -> str:
        return self.__prog

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
    def logger(self) -> logging.Logger:
        '''
        Logger.
        '''
        return logging.getLogger(self.prog)

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

    def __add_optional_version(self, argp: argp, root: add_command):
        if not isinstance(root, add_command):
            return

        if not isinstance(self.version, str):
            return

        version = self.version.strip()
        if not version:
            return

        argp.add_argument("--version",
                          action="version",
                          version=f"%(prog)s {version}")

    def __add_inner_parser_tail(self, argp: argp, root: add_command):
        if not isinstance(root, add_command):
            return

        def filter_optional_name(*name: str) -> Optional[str]:
            options = argp.filter_optional_name(*name)
            if len(options) > 0:
                for i in name:
                    if i in options:
                        return i
            return None

        def add_optional_level():

            def get_all_level_name() -> List[str]:
                return ["fatal", "error", "warn", "info", "debug"]

            group = argp.argument_group("logger optional arguments")
            group_level = group.add_mutually_exclusive_group()

            option_level = filter_optional_name("--level", "--log-level")
            if isinstance(option_level, str):
                group_level.add_argument(
                    option_level,
                    type=str,
                    nargs="?",
                    const="info",
                    default="info",
                    choices=get_all_level_name(),
                    dest="_log_level_str_",
                    help="Logger output level, default info.")

            for level in get_all_level_name():
                options = []
                if isinstance(filter_optional_name(f"-{level[0]}"), str):
                    options.append(f"-{level[0]}")
                if isinstance(filter_optional_name(f"--{level}"), str):
                    options.append(f"--{level}")
                elif isinstance(filter_optional_name(f"--{level}-level"), str):
                    options.append(f"--{level}-level")

                if not options:
                    continue
                group_level.add_argument(*options,
                                         action="store_const",
                                         const=level,
                                         dest="_log_level_str_",
                                         help=f"Logger level set to {level}.")

        def add_optional_stream():
            option = filter_optional_name("--log", "--log-file")
            if not isinstance(option, str):
                return

            group = argp.argument_group("logger optional arguments")
            group.add_argument(option,
                               type=str,
                               nargs=1,
                               default=[],
                               metavar="FILE",
                               action="extend",
                               dest="_log_files_",
                               help="Logger output to file.")

        def add_optional_format():
            option = filter_optional_name("--format", "--log-format")
            if not isinstance(option, str):
                return

            DEFAULT_FMT = "%(asctime)s %(process)d %(threadName)s"\
                " %(levelname)s %(funcName)s %(filename)s:%(lineno)s"\
                " %(message)s"

            group = argp.argument_group("logger optional arguments")
            group.add_argument(option,
                               type=str,
                               nargs="?",
                               const=DEFAULT_FMT,
                               default=None,
                               metavar="STRING",
                               dest="_log_format_",
                               help="Logger output format.")

        def add_optional_console():
            group = argp.argument_group("logger optional arguments")
            group_std = group.add_mutually_exclusive_group()

            option = filter_optional_name("--stdout", "--log-stdout")
            if isinstance(option, str):
                group_std.add_argument(option,
                                       const=sys.stdout,
                                       action="store_const",
                                       dest="_log_console_",
                                       help="Logger output to stdout.")

            option = filter_optional_name("--stderr", "--log-stderr")
            if isinstance(option, str):
                group_std.add_argument(option,
                                       const=sys.stderr,
                                       action="store_const",
                                       dest="_log_console_",
                                       help="Logger output to stderr.")

        add_optional_level()
        add_optional_stream()
        add_optional_format()
        add_optional_console()

    def __parse_logger(self, args: Namespace):
        # save debug level to local variable
        if hasattr(args, "_log_level_str_") and\
           isinstance(args._log_level_str_, str):
            level_name = args._log_level_str_.upper()
            self.logger.setLevel(logging._nameToLevel[level_name])

        formatter = logging.Formatter(
            fmt=args._log_format_ if hasattr(args, "_log_format_")
            and isinstance(args._log_format_, str) else None,
            datefmt=None)

        def addHandler(handler: logging.Handler):
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        if hasattr(args, "_log_console_") and args._log_console_ is not None:
            addHandler(logging.StreamHandler(stream=args._log_console_))

        for filename in args._log_files_:
            assert isinstance(filename, str)
            addHandler(logging.FileHandler(filename))

    def __add_parser(self, argp: argp, root: add_command, **kwargs):
        if not isinstance(root, add_command):
            return

        root.func(argp)
        self.__add_inner_parser_tail(argp, root)

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
            root = self.root

        assert isinstance(root, add_command)

        _arg = argp(**kwargs)
        self.__prog = _arg.prog
        self.__add_optional_version(_arg, root)
        self.__add_parser(_arg, root, **kwargs)

        autocomplete(_arg)
        args = _arg.parse_args(argv)
        assert isinstance(args, Namespace)
        self.__parse_logger(args)
        self.args = args
        return self.args

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
            if isinstance(sub_name, str):

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
            root = self.root

        if not isinstance(root, add_command):
            self.logger.debug("cannot find root")
            return ENOENT

        kwargs.pop("prog", None)  # Please do not specify prog
        args = self.parse(root, argv, **kwargs)
        self.logger.debug(f"{args}")

        try:
            version = self.version
            if isinstance(version, str):
                # Output version for the debug level. Internal log
                # items are debug level only, except for errors.
                self.logger.debug(f"version: {version}")

            return self.__run(args, root)
        except KeyboardInterrupt:
            return EINTR
        except BaseException:
            self.logger.exception("Something went wrong:")
            return 10000
