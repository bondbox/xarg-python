#!/usr/bin/python3
# coding:utf-8
# Copyright (c) 2023 ZouMingzhe <zoumingzhe@qq.com>

from xarg import __version__ as version
from xarg import xarg


def main():
    _arg = xarg("xarg",
                description="hello the world",
                epilog="This is the xarg project test command-line.")
    _arg.add_argument('-v',
                      '--version',
                      action='version',
                      version=f'%(prog)s {version}')
    _arg.add_subparsers(dest="sub", required=True)
    _sub = _arg.add_parser("opt")
    _sub.add_opt("-x")
    _sub.add_opt("-arg")
    _sub.add_opt("-o", "--opt")
    _sub = _arg.add_parser("opt-on")
    _sub.add_opt_on("--opt-on")
    _sub = _arg.add_parser("opt-off")
    _sub.add_opt_off("--opt-off")
    _sub = _arg.add_parser("pos-default")
    _sub.add_pos("pos")
    _sub = _arg.add_parser("pos-1")
    _sub.add_pos("pos_1", nargs=1)
    _sub = _arg.add_parser("pos-2")
    _sub.add_pos("pos_2", nargs=2)
    _sub = _arg.add_parser("pos-0+")
    _sub.add_pos("pos_0+", nargs=0)
    _sub = _arg.add_parser("pos-1+")
    _sub.add_pos("pos_1+", nargs=-1)
    _sub = _arg.add_parser("pos-0-or-1")
    _sub.add_pos("pos_0_or_1")
    _sub = _arg.add_parser("sub_opt")
    _sub.add_subparsers()
    _sub2 = _sub.add_parser("opt-on")
    _sub2.add_opt_on("--opt-on")
    _sub2 = _sub.add_parser("opt-off")
    _sub2.add_opt_off("--opt-off")
    print(_arg.parse_args())
