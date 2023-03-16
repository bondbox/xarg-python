import unittest
from argparse import ArgumentParser
from xarg import ArgParser


class TestArgParser(unittest.TestCase):

    def setUp(self):
        self.parser = ArgumentParser()
        self.ArgParser = ArgParser(self.parser)

    def test_add_argument_short(self):
        self.ArgParser.add_argument('-x', '--xx', help='optional argument')
        args = self.ArgParser.parse_args('-x value'.split())
        self.assertEqual(args.xx, 'value')

    def test_add_argument_long(self):
        self.ArgParser.add_argument('-x', '--xx', help='optional argument')
        args = self.ArgParser.parse_args('--xx value'.split())
        self.assertEqual(args.xx, 'value')

    def test_add_opt_on(self):
        self.ArgParser.add_opt_on('-x', help='boolean optional argument')
        args = self.ArgParser.parse_args('-x'.split())
        self.assertEqual(args.x, True)

    def test_add_opt_off(self):
        self.ArgParser.add_opt_off('-x', help='boolean optional argument')
        args = self.ArgParser.parse_args(''.split())
        self.assertEqual(args.x, True)

    def test_add_opt_nargs1_args0(self):
        self.ArgParser.add_opt('--dest', nargs=1, help='optional argument')
        args = self.ArgParser.parse_args('--dest'.split())
        self.assertEqual(args.dest, None)

    def test_add_opt_nargs1_args1(self):
        self.ArgParser.add_opt('--dest', nargs=1, help='optional argument')
        args = self.ArgParser.parse_args('--dest value'.split())
        self.assertEqual(args.dest, 'value')

    def test_add_pos_args0(self):
        self.ArgParser.add_pos('dest', help='positional argument')
        args = self.ArgParser.parse_args(''.split())
        self.assertEqual(args.dest, None)

    def test_add_pos_args1(self):
        self.ArgParser.add_pos('dest', help='positional argument')
        args = self.ArgParser.parse_args('value'.split())
        self.assertEqual(args.dest, 'value')

    def test_add_pos_nargs1p_args0(self):
        self.ArgParser.add_pos('dest', nargs=-1)
        self.assertRaises(BaseException, self.ArgParser.parse_args, ''.split())

    def test_add_pos_nargs1p_args1(self):
        self.ArgParser.add_pos('dest', type=str, nargs=-1)
        args = self.ArgParser.parse_args('123'.split())
        self.assertEqual(args.dest, ['123'])

    def test_add_pos_nargs0_args0(self):
        self.ArgParser.add_pos('dest', nargs=0)
        args = self.ArgParser.parse_args(''.split())
        self.assertEqual(args.dest, [])

    def test_add_pos_nargs0_args2(self):
        self.ArgParser.add_pos('dest', type=float, nargs=0)
        args = self.ArgParser.parse_args('1.23 4.56'.split())
        self.assertEqual(args.dest, [1.23, 4.56])

    def test_add_pos_nargs1_args0(self):
        self.ArgParser.add_pos('dest', nargs=1)
        args = self.ArgParser.parse_args(''.split())
        self.assertEqual(args.dest, None)

    def test_add_pos_nargs1_args1(self):
        self.ArgParser.add_pos('dest', nargs=1)
        args = self.ArgParser.parse_args('value'.split())
        self.assertEqual(args.dest, 'value')

    def test_add_pos_nargs3_args3(self):
        self.ArgParser.add_pos('dest', type=int, nargs=3)
        args = self.ArgParser.parse_args('1 2 3'.split())
        self.assertEqual(args.dest, [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
