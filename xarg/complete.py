#!/usr/bin/python3
# coding:utf-8

from base64 import b16decode
from base64 import b16encode
from configparser import ConfigParser
import os
import shutil
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple

from tabulate import tabulate

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from .util import URL_PROG
from .util import __package_name__
from .util import __prog_complete__
from .util import __version__

USER_BASH_COMPLETION_CFG = "~/.bash_completion"
USER_BASH_COMPLETION_DIR = "~/.bash_completion.d"


def init_bash():
    bash_completion_code = """
for bcfile in ~/.bash_completion.d/* ; do
  source ${bcfile}
done
"""
    bash_completion_path = os.path.expanduser(USER_BASH_COMPLETION_CFG)
    bash_completion_hook = os.path.expanduser(USER_BASH_COMPLETION_DIR)
    if not os.path.exists(bash_completion_hook):
        os.makedirs(bash_completion_hook)
    with open(bash_completion_path, "r") as fh:
        if bash_completion_code in fh.read():
            return
    with open(bash_completion_path, "a") as fh:
        fh.write(f"\n{bash_completion_code}\n")


def update_bash(cmd: str) -> int:
    bash_completion_hook = os.path.expanduser(USER_BASH_COMPLETION_DIR)
    name = b16encode(cmd.encode()).decode()
    path = os.path.join(bash_completion_hook, f"{__prog_complete__}-{name}")
    return os.system(f"register-python-argcomplete {cmd} > {path}")


def list_bash() -> Set[str]:
    cmds: Set[str] = set()
    bash_completion_hook = os.path.expanduser(USER_BASH_COMPLETION_DIR)
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
        self.__pkg_files: List[str] = []
        self.__have_file = False
        with os.popen(f"pip show --files {name}") as fd:
            for line in fd.readlines():
                if not self.__have_file:
                    title, value = line.split(":", 1)
                    if title != "Files":
                        self.__pkg_infos[title] = value.strip()
                    else:
                        self.__have_file = True
                else:
                    path = line.strip()
                    self.__pkg_files.append(path)
                    if "entry_points.txt" in path:
                        self.__entry_points = path

    @property
    def name(self) -> str:
        return self.__pkg_infos["Name"]

    @property
    def version(self) -> str:
        return self.__pkg_infos["Version"]

    @property
    def requires(self) -> Set[str]:
        return {i.strip() for i in self.__pkg_infos["Requires"].split(",")}

    @property
    def required_by(self) -> Set[str]:
        return {i.strip() for i in self.__pkg_infos["Required-by"].split(",")}

    @property
    def console_scripts(self) -> Set[str]:
        try:
            path = os.path.join(
                self.__pkg_infos["Location"], self.__entry_points)
            config = ConfigParser()
            config.read(path)
            return {i for i in config["console_scripts"]}
        except Exception:
            return set()


@add_command("init", help="Enable completion.")
def add_cmd_init(_arg: argp):
    pass


@run_command(add_cmd_init)
def run_cmd_init(cmds: commands) -> int:
    retcode = os.system("activate-global-python-argcomplete -y")
    if retcode != 0:
        return retcode
    init_bash()
    return 0


@add_command("update", help="Update completion config.")
def add_cmd_update(_arg: argp):
    pass


@run_command(add_cmd_update)
def run_cmd_update(cmds: commands) -> int:

    def update_complete(name: str):
        cmds.stdout(f"package: {name}")
        info = package_info(name)
        for cmd in info.console_scripts:
            cmds.stdout(f" └ command: {cmd}")
            update_bash(cmd)

    pkgi = package_info(__package_name__)
    for required in pkgi.required_by:
        update_complete(required)
    update_bash(__prog_complete__)
    cmds.stdout("Please log in your shell again.")
    return 0


@add_command("list", help="List all completion.")
def add_cmd_list(_arg: argp):
    pass


@run_command(add_cmd_list)
def run_cmd_list(cmds: commands) -> int:
    table: List[Tuple[str, str, str]] = []
    for cmd in list_bash():
        which = shutil.which(cmd)
        table.append(
            ("bash", cmd, which if isinstance(which, str) else "None"))
    cmds.stdout(tabulate(table, headers=["shell", "command", "which"]))
    return 0


@add_command(__prog_complete__)
def add_cmd(_arg: argp):
    pass


@run_command(add_cmd, add_cmd_init, add_cmd_update, add_cmd_list)
def run_cmd(cmds: commands) -> int:
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(
        root=add_cmd,
        argv=argv,
        description="Simple command-line tool based on argparse.",
        epilog=f"For more, please visit {URL_PROG}.")
