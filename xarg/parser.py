#!/usr/bin/python3
# coding:utf-8

from argparse import ArgumentParser
from argparse import _ArgumentGroup
from argparse import _SubParsersAction
from typing import Optional

from .util import URL_PROG


class checker():

    prefix_chars = "-"

    @classmethod
    def check_name_pos(cls, fn):
        '''
        check positional argument name
        '''

        def inner(self, name: str, **kwargs):
            assert isinstance(name, str) and name[0] not in cls.prefix_chars,\
                f"{name} is not a positional argument name"
            return fn(self, name, **kwargs)

        return inner

    @classmethod
    def check_name_opt(cls, fn):
        '''
        check optional argument name
        '''

        def inner(self, *name: str, **kwargs):
            # 1. check short form optional argument ("-x")
            # 2. check long form optional argument ("--xx")
            # 3. only short form or long form or short form + long form
            # 模棱两可的数据（-1可以是一个负数的位置参数）
            for n in name:
                assert isinstance(n, str) and n[0] in cls.prefix_chars,\
                    f"{n} is not an optional argument name"
            return fn(self, *name, **kwargs)

        return inner

    @classmethod
    def check_nargs_opt(cls, fn):
        '''
        nargs hook function:
            nargs < -1: using "?", 0 or 1 argument, default value
            nargs = -1: using "+", arguments list, at least 1
            nargs = 0: using "*", arguments list, allow to be empty
            nargs = 1: redirect to "?", 0 or 1 argument
            nargs > 1: N arguments list
        '''

        def inner(self, *args, **kwargs):
            _nargs = kwargs.get("nargs", -2)
            if isinstance(_nargs, int) and _nargs < 2:
                _nargs = {1: "?", 0: "*", -1: "+"}.get(_nargs, "?")
            kwargs.update({"nargs": _nargs})
            return fn(self, *args, **kwargs)

        return inner


class argp(ArgumentParser):
    '''
    Simple command-line tool based on argparse.
    '''

    def __init__(self,
                 prog: Optional[str] = None,
                 usage: Optional[str] = None,
                 description: Optional[str] = "Command-line based on xarg.",
                 epilog: Optional[str] = f"For more, please visit {URL_PROG}",
                 **kwargs):
        kwargs.setdefault("prog", prog)
        kwargs.setdefault("usage", usage)
        kwargs.setdefault("description", description)
        kwargs.setdefault("epilog", epilog)
        ArgumentParser.__init__(self, **kwargs)

    def argument_group(self,
                       title: Optional[str] = None,
                       description: Optional[str] = None,
                       **kwargs) -> _ArgumentGroup:
        '''
        Find the created argument group by title, create if not exist.
        '''
        for group in self._action_groups:
            if title == group.title:
                return group
        return self.add_argument_group(title, description, **kwargs)

    @checker.check_name_opt
    def filter_optional_name(self, *name: str) -> set:
        '''
        Filter defined optional argument name.
        '''
        option_strings = set()
        for action in self._get_optional_actions():
            option_strings.update(action.option_strings)
        return set(name) - option_strings

    @checker.check_name_pos
    def add_pos(self, name: str, **kwargs) -> None:
        '''
        Add positional argument.
        '''
        assert "dest" not in kwargs,\
            "dest supplied twice for positional argument"
        self.add_argument(name, **kwargs)

    @checker.check_name_opt
    @checker.check_nargs_opt
    def add_opt(self, *name: str, **kwargs) -> None:
        '''
        Add optional argument.
        '''
        self.add_argument(*name, **kwargs)

    @checker.check_name_opt
    def add_opt_on(self, *name: str, **kwargs) -> None:
        '''
        Add boolean optional argument, default value is False.
        '''
        kwargs.update({"action": "store_true"})
        for key in ("type", "nargs", "const", "default", "choices"):
            assert key not in kwargs, f"'{key}' is an invalid argument"
        self.add_argument(*name, **kwargs)

    @checker.check_name_opt
    def add_opt_off(self, *name: str, **kwargs) -> None:
        '''
        Add boolean optional argument, default value is True.
        '''
        kwargs.update({"action": "store_false"})
        for key in ("type", "nargs", "const", "default", "choices"):
            assert key not in kwargs, f"'{key}' is an invalid argument"
        self.add_argument(*name, **kwargs)

    def add_subparsers(self, *args, **kwargs) -> _SubParsersAction:
        '''
        Add subparsers.
        '''
        # subparser: cannot have multiple subparser arguments
        kwargs.setdefault("title", "subcommands")
        kwargs.setdefault("description", None)
        kwargs.setdefault("dest", f"subcmd_{self.prog}")
        kwargs.setdefault("help", None)
        kwargs.setdefault("metavar", None)
        return ArgumentParser.add_subparsers(self, *args, **kwargs)
