#!/usr/bin/python3
# coding:utf-8

from base64 import b16decode
from base64 import b16encode
from configparser import ConfigParser
import os
import shutil
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Union

from tabulate import tabulate

from .actuator import add_command
from .actuator import commands
from .actuator import run_command
from .parser import argp
from .util import URL_PROG
from .util import __package_name__
from .util import __prog_complete__
from .util import __version__
from .util import singleton

USER_BASH_COMPLETION_CFG = "~/.bash_completion"
USER_BASH_COMPLETION_DIR = "~/.bash_completion.d"


def enable_bash():

    def update_code():
        bash_completion_path = os.path.expanduser(USER_BASH_COMPLETION_CFG)
        bash_completion_hook = os.path.expanduser(USER_BASH_COMPLETION_DIR)
        bash_completion_code = """
for bcfile in ~/.bash_completion.d/* ; do
  source ${bcfile}
done
"""
        if not os.path.exists(bash_completion_hook):
            os.makedirs(bash_completion_hook)
        with open(bash_completion_path, "r") as fh:
            if bash_completion_code in fh.read():
                return
        with open(bash_completion_path, "a") as fh:
            fh.write(f"\n{bash_completion_code}\n")

    update_code()
    update_bash(__prog_complete__)


def update_bash(cmd: str) -> int:
    bash_completion_hook = os.path.expanduser(USER_BASH_COMPLETION_DIR)
    name = b16encode(cmd.encode()).decode()
    path = os.path.join(bash_completion_hook, f"{__prog_complete__}-{name}")
    return os.system(f"register-python-argcomplete {cmd} > {path}")


def remove_bash(cmd: str) -> bool:
    bash_completion_hook = os.path.expanduser(USER_BASH_COMPLETION_DIR)
    name = b16encode(cmd.encode()).decode()
    path = os.path.join(bash_completion_hook, f"{__prog_complete__}-{name}")
    if os.path.isfile(path):
        os.remove(path)
    return not os.path.exists(path)


def list_bash() -> Set[str]:
    cmds: Set[str] = set()
    bash_completion_hook = os.path.expanduser(USER_BASH_COMPLETION_DIR)
    if not os.path.exists(bash_completion_hook):
        os.makedirs(bash_completion_hook)
    for item in os.listdir(bash_completion_hook):
        if not os.path.isfile(os.path.join(bash_completion_hook, item)):
            continue
        keys = item.split("-", 1)
        if len(keys) == 2 and keys[0] == __prog_complete__:
            cmds.add(b16decode(keys[1]).decode())
    return cmds


class package_info:

    def __init__(self, name: str):
        self.__pkg_infos: Dict[str, str] = {}
        self.__pkg_files: set[str] = set()
        self.__have_file = False
        with os.popen(f"pip show --files {name}") as fd:
            for line in fd.readlines():
                if not self.__have_file:
                    title, value = line.split(":", 1)
                    if title != "Files":
                        self.__pkg_infos[title] = value.strip()
                    else:
                        self.__location = self.__pkg_infos["Location"]
                        self.__have_file = True
                else:
                    path = os.path.join(self.location, line.strip())
                    abspath = os.path.abspath(path)
                    self.__pkg_files.add(abspath)
                    if "entry_points.txt" in abspath:
                        self.__entry_points = abspath

    @property
    def name(self) -> str:
        return self.__pkg_infos["Name"]

    @property
    def version(self) -> str:
        return self.__pkg_infos["Version"]

    @property
    def location(self) -> str:
        return self.__location

    @property
    def requires(self) -> Set[str]:
        return {i.strip() for i in self.__pkg_infos["Requires"].split(",")}

    @property
    def required_by(self) -> Set[str]:
        return {i.strip() for i in self.__pkg_infos["Required-by"].split(",")}

    @property
    def files(self) -> Set[str]:
        return self.__pkg_files

    @property
    def console_scripts(self) -> Set[str]:
        try:
            config = ConfigParser()
            config.read(self.__entry_points)
            return {i for i in config["console_scripts"]}
        except Exception:
            return set()


@singleton
class collections:

    def __init__(self):
        info = package_info(__package_name__)
        self.__pkgs: Set[str] = {i for i in info.required_by}
        self.__cmds: Set[str] = {__prog_complete__}
        for pkg in self.__pkgs:
            pkgi = package_info(pkg)
            for cmd in pkgi.console_scripts:
                self.__cmds.add(cmd)

    @property
    def cmds(self) -> Iterable[str]:
        return iter(self.__cmds)


@add_command("enable", help="Enable completion.")
def add_cmd_enable(_arg: argp):
    pass


@run_command(add_cmd_enable)
def run_cmd_enable(cmds: commands) -> int:
    which = shutil.which("activate-global-python-argcomplete")
    command = f"{which} --user --yes"
    cmds.logger.info(command)
    retcode = os.system(command)
    if retcode != 0:
        return retcode
    enable_bash()
    return 0


@add_command("update", help="Update completion config.")
def add_cmd_update(_arg: argp):
    group_script = _arg.argument_group("Specify update command or script")
    group_script.add_argument("--script", type=str, nargs=1, metavar="PATH",
                              dest="_commands_", action="extend",
                              help="Specify script path.")
    group_script.add_argument(type=str, nargs="*", metavar="command",
                              dest="_commands_", action="extend",
                              help="Specify command.")


@run_command(add_cmd_update)
def run_cmd_update(cmds: commands) -> int:
    if len(cmds.args._commands_) == 0:
        cmds.args._commands_ = collections().cmds
    for cmd in set(cmds.args._commands_):
        if shutil.which(cmd) is None:
            cmds.stderr(f"Non existent command or script: {cmd}")
            continue
        cmds.stdout(f"Update command or script: {cmd}")
        update_bash(cmd)
    cmds.stdout("Please restart your shell or source the file to activate it.")
    cmds.stdout(f"Bash: source {os.path.expanduser(USER_BASH_COMPLETION_CFG)}")
    return 0


@add_command("remove", help="Remove completion config.")
def add_cmd_remove(_arg: argp):
    allowed = list(list_bash())
    group_script = _arg.argument_group("Specify remove command or script")
    mgroup_script = group_script.add_mutually_exclusive_group()
    mgroup_script.add_argument("--auto-clean", dest="_clean_",
                               action="store_true",
                               help="Clean invalid commands or scripts.")
    mgroup_script.add_argument("--all", const=allowed,
                               dest="_commands_", action="store_const",
                               help="Remove all commands or scripts.")
    group_script.add_argument(type=str, nargs="*", metavar="command",
                              dest="_commands_", action="extend",
                              help="Specify command or script.",
                              choices=allowed + [[]])


@run_command(add_cmd_remove)
def run_cmd_remove(cmds: commands) -> int:
    if cmds.args._clean_:
        assert isinstance(cmds.args._commands_, list)
        for cmd in list_bash():
            if cmd in cmds.args._commands_:
                continue
            if shutil.which(cmd) is None:
                cmds.args._commands_.append(cmd)
    for cmd in set(cmds.args._commands_):
        cmds.stdout(f"Remove command or script: {cmd}")
        assert remove_bash(cmd)
    return 0


@add_command("list", help="List all completion.")
def add_cmd_list(_arg: argp):
    pass


@run_command(add_cmd_list)
def run_cmd_list(cmds: commands) -> int:
    table: Dict[str, Dict[str, Union[None, str, Set[str]]]] = {}

    def update_table(cmd: str, shell: str):
        if cmd not in table:
            table[cmd] = {"which": shutil.which(cmd), "shell": set()}
        shell_set = table[cmd]["shell"]
        assert isinstance(shell_set, set)
        shell_set.add(shell)

    def output_table() -> List[Tuple[str, str, str]]:
        datas: List[Tuple[str, str, str]] = []
        for k, v in table.items():
            which = v["which"] if v["which"] is not None else "None"
            shell = v["shell"]
            assert isinstance(which, str)
            assert isinstance(shell, set)
            datas.append((k, which, ", ".join(shell)))
        datas.sort(key=lambda line: line[0])
        datas.insert(0, ("command", "which", "shell"))
        return datas

    for cmd in list_bash():
        update_table(cmd, "bash")
    cmds.stdout(tabulate(output_table(), headers="firstrow"))
    return 0


@add_command(__prog_complete__)
def add_cmd(_arg: argp):
    pass


@run_command(add_cmd, add_cmd_enable, add_cmd_update, add_cmd_remove,
             add_cmd_list)
def run_cmd(cmds: commands) -> int:
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(
        root=add_cmd,
        argv=argv,
        description="Tab completion management.",
        epilog=f"For more, please visit {URL_PROG}.")
