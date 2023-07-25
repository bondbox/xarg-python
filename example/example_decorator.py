#!/usr/bin/python3
# coding:utf-8

from typing import List
from typing import Optional

from xarg import argp
from xarg import commands, add_command, run_command


@add_command('key', help="item key")
def cmd_key(argp: argp):
    # print("key", argp)
    pass


@add_command('value', help="item value")
def cmd_val(argp: argp):
    # print("value", argp)
    pass


@add_command('get', help="get item")
def cmd_get(argp: argp):
    # print("get", argp)
    pass


@run_command(cmd_get, cmd_key)
def run_get(args) -> int:
    print("run get", args)
    return 0


@add_command('set', help="set item")
def cmd_set(argp: argp):
    # print("set", argp)
    pass


@run_command(cmd_set, cmd_key, cmd_val)
def run_set(args) -> int:
    print("run set", args)
    return 0


@add_command('del', help="delete item")
def cmd_del(argp: argp):
    # print("del", argp)
    pass


@run_command(cmd_del)
def run_del(args) -> int:
    print("run del", args)
    return 0


@add_command('example')
def cmd(argp: argp):
    # print("example", argp)
    argp.add_opt_on('-d', '--debug', help="show debug information")


@run_command(cmd, cmd_get, cmd_set, cmd_del)
def run(args) -> int:
    print("run example", args)
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    return commands().run(
        ['-d', 'set', 'value'],
        prog="xarg-example",
        description="Simple command-line tool based on argparse.")


if __name__ == '__main__':
    main()
