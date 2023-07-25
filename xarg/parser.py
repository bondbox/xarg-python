#!/usr/bin/python3
# coding:utf-8

from argparse import ArgumentParser
from argparse import _SubParsersAction
from typing import Optional

from .checker import check_name_opt
from .checker import check_name_pos
from .checker import check_nargs_opt


class argp(ArgumentParser):
    '''
    Simple command-line tool based on argparse.
    '''

    def __init__(self,
                 prog: Optional[str] = None,
                 usage: Optional[str] = None,
                 description: Optional[str] = None,
                 epilog: Optional[str] = None,
                 **kwargs):
        kwargs.setdefault("prog", prog)
        kwargs.setdefault("usage", usage)
        kwargs.setdefault("description", description)
        kwargs.setdefault("epilog", epilog)
        ArgumentParser.__init__(self, **kwargs)

    @check_name_pos
    def add_pos(self, name: str, **kwargs) -> None:
        '''
        add positional argument
        '''
        assert 'dest' not in kwargs,\
            "dest supplied twice for positional argument"
        self.add_argument(name, **kwargs)

    @check_name_opt
    @check_nargs_opt
    def add_opt(self, *name: str, **kwargs) -> None:
        '''
        add optional argument
        '''
        self.add_argument(*name, **kwargs)

    @check_name_opt
    def add_opt_on(self, *name: str, **kwargs) -> None:
        '''
        add boolean optional argument, default value is False
        '''
        kwargs.update({"action": 'store_true'})
        for key in ("type", "nargs", "const", "default", "choices"):
            assert key not in kwargs, f"'{key}' is an invalid argument"
        self.add_argument(*name, **kwargs)

    @check_name_opt
    def add_opt_off(self, *name: str, **kwargs) -> None:
        '''
        add boolean optional argument, default value is True
        '''
        kwargs.update({"action": 'store_false'})
        for key in ("type", "nargs", "const", "default", "choices"):
            assert key not in kwargs, f"'{key}' is an invalid argument"
        self.add_argument(*name, **kwargs)

    def add_subparsers(self, *args, **kwargs) -> _SubParsersAction:
        '''
        enable subparsers
        '''
        # subparser: cannot have multiple subparser arguments
        kwargs.setdefault("dest", f"subcmd_{self.prog}")
        kwargs.setdefault('parser_class', type(self))
        kwargs.setdefault("help", "sub-command list")
        return ArgumentParser.add_subparsers(self, *args, **kwargs)
