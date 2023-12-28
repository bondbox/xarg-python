# coding:utf-8

from argparse import Namespace
from errno import EINTR
from errno import ENOENT
import logging
import sys
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

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
        self.__name: str = name
        self.__prev: add_command = self
        self.__cmds: commands = commands()
        self.__options: Dict[str, Any] = kwargs
        self.__bind: Optional[run_command] = None
        self.__subs: Optional[Tuple[add_command, ...]] = None

    def __call__(self, cmd_func: Callable[[argp], None]):
        self.__func = cmd_func
        return self

    @property
    def func(self):
        return self.__func

    @property
    def name(self):
        return self.__name

    @property
    def root(self):
        root = self.__prev
        while root.prev != root:
            root = root.prev
        return root

    @property
    def prev(self):
        return self.__prev

    @prev.setter
    def prev(self, value: "add_command"):
        assert isinstance(value, add_command)
        self.__prev = value

    @property
    def cmds(self):
        return self.__cmds

    @property
    def options(self):
        return self.__options

    @property
    def bind(self):
        return self.__bind

    @bind.setter
    def bind(self, value: "run_command"):
        assert isinstance(value, run_command)
        self.__bind = value

    @property
    def subs(self):
        return self.__subs

    @subs.setter
    def subs(self, value: Tuple["add_command", ...]):
        self.__subs = value

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
            sub.prev = cmd_bind

        cmd_bind.bind = self
        cmd_bind.subs = subs
        commands().root = cmd_bind.root
        self.__bind: add_command = cmd_bind

    def __call__(self, run_func: Callable[["commands"], int]):
        self.__func = run_func
        return self

    @property
    def func(self):
        return self.__func

    @property
    def bind(self) -> add_command:
        return self.__bind


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

    LOGGER_ARGUMENT_GROUP = "logger options"

    def __init__(self, version: Optional[str] = None,
                 enable_logger: bool = True):
        assert isinstance(version, str) or version is None
        assert isinstance(enable_logger, bool)
        self.__prog: str = "xarg"
        self.__root: Optional[add_command] = None
        self.__args: Namespace = Namespace()
        self.__version: Optional[str] = version
        self.__enable_logger: bool = enable_logger

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
        assert isinstance(value, add_command)
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
        assert isinstance(value, Namespace)
        self.__args = value

    @property
    def version(self) -> Optional[str]:
        '''
        Custom version for "-v" or "--version" output.
        '''
        return self.__version

    @version.setter
    def version(self, value: str):
        assert isinstance(value, str)
        _version = value.strip()
        self.__version = _version

    @property
    def enable_logger(self) -> bool:
        return self.__enable_logger

    @enable_logger.setter
    def enable_logger(self, value: bool):
        assert isinstance(value, bool)
        self.__enable_logger = value

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

    def __add_optional_version(self, argp: argp):
        version = self.version
        if not isinstance(version, str):
            return

        options = argp.filter_optional_name("-v", "--version")
        if len(options) > 0:
            argp.add_argument(*options, action="version",
                              version=f"%(prog)s {version.strip()}")

    def __add_inner_parser_tail(self, argp: argp):

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

            group = argp.argument_group(self.LOGGER_ARGUMENT_GROUP)
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

            group = argp.argument_group(self.LOGGER_ARGUMENT_GROUP)
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

            group = argp.argument_group(self.LOGGER_ARGUMENT_GROUP)
            group.add_argument(option,
                               type=str,
                               nargs="?",
                               const=DEFAULT_FMT,
                               default=None,
                               metavar="STRING",
                               dest="_log_format_",
                               help="Logger output format.")

        def add_optional_console():
            group = argp.argument_group(self.LOGGER_ARGUMENT_GROUP)
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

        if self.enable_logger:
            add_optional_level()
            add_optional_stream()
            add_optional_format()
            add_optional_console()

    def __parse_logger(self, args: Namespace):
        if not self.enable_logger:
            return

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

        if hasattr(args, "_log_files_"):
            for filename in args._log_files_:
                assert isinstance(filename, str)
                addHandler(logging.FileHandler(filename))

    def __add_parser(self, _map: Dict[add_command, argp],
                     arg_root: argp, cmd_root: add_command, **kwargs):
        assert isinstance(cmd_root, add_command)
        assert cmd_root not in _map
        _map[cmd_root] = arg_root

        if not cmd_root.subs or len(cmd_root.subs) <= 0:
            return

        _sub = arg_root.add_subparsers(dest=cmd_root.sub_dest)
        for sub in cmd_root.subs:
            assert isinstance(sub, add_command)
            for key, value in kwargs.items():
                sub.options.setdefault(key, value)
            sub.options.setdefault("epilog", arg_root.epilog)
            sub.options.setdefault("prev_parser", arg_root)
            _arg: argp = _sub.add_parser(sub.name, **sub.options)
            self.__add_parser(_map, _arg, sub)

    def __add_option(self, _map: Dict[add_command, argp]):
        for _cmd, _arg in _map.items():
            _cmd.func(_arg)
            self.__add_inner_parser_tail(_arg)

    def parse(self, root: Optional[add_command] = None,
              argv: Optional[Sequence[str]] = None, **kwargs) -> Namespace:
        '''
        Parse the command line.
        '''
        if root is None:
            root = self.root
        assert isinstance(root, add_command)

        _map: Dict[add_command, argp] = dict()
        _arg = argp(argv=argv, **kwargs)
        self.__prog = _arg.prog
        self.__add_optional_version(_arg)
        # To support preparse_from_sys_argv(), all subparsers must be added
        # first. Otherwise, an error will occur during the help action.
        self.__add_parser(_map, _arg, root, **kwargs)
        self.__add_option(_map)

        args = _arg.parse_args(args=argv)
        assert isinstance(args, Namespace)
        self.__parse_logger(args)
        self.args = args
        return self.args

    def __run(self, args: Namespace, root: add_command) -> int:
        assert isinstance(root, add_command)
        assert isinstance(root.bind, run_command)

        ret = root.bind.func(self)
        if ret != 0 and ret is not None:
            return ret

        if hasattr(args, root.sub_dest):
            sub_dest = getattr(args, root.sub_dest)
            if isinstance(sub_dest, str):
                assert isinstance(root.subs, (list, tuple))
                for sub in root.subs:
                    assert isinstance(sub, add_command)
                    if sub.name == sub_dest:
                        return self.__run(args, sub)
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
