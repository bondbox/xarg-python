# coding:utf-8

from argparse import Namespace
from errno import ENOENT
import sys
import unittest

import mock

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command


@add_command("list", help="test list")
def add_cmd_list(_arg: argp):
    commands().stderr("error")
    pass


@run_command(add_cmd_list)
def run_cmd_list(cmds: commands) -> int:
    cmds.logger.warn("incomplete")
    return -1


@add_command("example")
def add_cmd(_arg: argp):
    commands().stdout("test")
    pass


@run_command(add_cmd, add_cmd_list)
def run_cmd(cmds: commands) -> int:
    cmds.logger.debug("main")
    return 0


class Test_decorator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.cmds = commands()
        self.cmds.version = "3.2.1"

    def tearDown(self):
        pass

    def test_root(self):
        ret = self.cmds.run(argv="--debug".split())
        self.assertEqual(ret, 0)

    def test_parse_root(self):
        ret = self.cmds.parse(argv="--debug".split())
        self.assertIsInstance(ret, Namespace)

    def test_run_root_error(self):
        ret = self.cmds.run(mock.Mock(), argv="--debug".split())
        self.assertEqual(ret, ENOENT)

    @mock.patch.object(argp, "filter_optional_name")
    def test_filter_optional_name(self, mock_filter_optional_name: mock.Mock):
        mock_filter_optional_name.return_value = []
        ret = self.cmds.run(add_cmd, "".split(), prog="example")
        self.assertEqual(ret, 0)

    @mock.patch.object(sys, "exit")
    def test_help_optional_h(self, mock_exit: mock.Mock):
        mock_exit.side_effect = [Exception("xarg-test")]
        self.assertRaises(Exception, self.cmds.run, add_cmd, "-h".split())
        mock_exit.assert_called_once_with(0)

    @mock.patch.object(sys, "exit")
    def test_help_optional_help(self, mock_exit: mock.Mock):
        mock_exit.side_effect = [Exception("xarg-test")]
        self.assertRaises(Exception, self.cmds.run, add_cmd_list,
                          "--help".split())
        mock_exit.assert_called_once_with(0)

    def test_subcommand_list(self):
        ret = self.cmds.run(add_cmd, "list".split(), prog="example")
        self.assertEqual(ret, -1)


if __name__ == "__main__":
    unittest.main()
