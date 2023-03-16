import unittest
from argparse import ArgumentParser
from xarg import ArgSubParser, ArgParser


class TestArgSubParser(unittest.TestCase):

    def setUp(self):
        self.parser = ArgumentParser()
        self.ArgSubParser = ArgSubParser('arg', self.parser)

    def test_add_parser(self):
        self.ArgSubParser.add_subparsers()
        _sub_parser = self.ArgSubParser.add_parser('sub')
        _sub_parser.add_pos('dest', help='positional argument')
        args = self.parser.parse_args(['sub', 'value'])
        self.assertEqual(args.subcmd_arg, 'sub')
        self.assertEqual(args.dest, 'value')

    def test_add_parser_twice(self):
        self.ArgSubParser.add_subparsers()
        _sub_parser1 = self.ArgSubParser.add_parser('sub')
        _sub_parser2 = self.ArgSubParser.add_parser('sub')
        self.assertEqual(_sub_parser1, _sub_parser2)


if __name__ == '__main__':
    unittest.main()
