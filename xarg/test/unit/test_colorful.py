# coding:utf-8

import unittest

from xarg import Back
from xarg import Fore
from xarg import Style
from xarg import color
from xarg import commands


class test_safile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_bold(self):
        text1 = color("unittest bold")
        text2 = color.bold(text1)
        text1.style = {Style.BRIGHT}
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_dim(self):
        text1 = color("unittest dim")
        text2 = color.dim(text1)
        text1.style = {Style.DIM}
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_normal(self):
        text1 = color("unittest normal")
        text2 = color.normal(text1)
        text1.style = {Style.NORMAL}
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_black(self):
        text1 = color("unittest black")
        text2 = color.black(text1)
        text1.foreground = Fore.BLACK
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_red(self):
        text1 = color("unittest red")
        text2 = color.red(text1)
        text1.foreground = Fore.RED
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_green(self):
        text1 = color("unittest green")
        text2 = color.green(text1)
        text1.foreground = Fore.GREEN
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_yellow(self):
        text1 = color("unittest yellow")
        text2 = color.yellow(text1)
        text1.foreground = Fore.YELLOW
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_blue(self):
        text1 = color("unittest blue")
        text2 = color.blue(text1)
        text1.foreground = Fore.BLUE
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_magenta(self):
        text1 = color("unittest magenta")
        text2 = color.magenta(text1)
        text1.foreground = Fore.MAGENTA
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_cyan(self):
        text1 = color("unittest cyan")
        text2 = color.cyan(text1)
        text1.foreground = Fore.CYAN
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_white(self):
        text1 = color("unittest white")
        text2 = color.white(text1)
        text1.foreground = Fore.WHITE
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_lightblack(self):
        text1 = color("unittest lightblack")
        text2 = color.lightblack(text1)
        text1.foreground = Fore.LIGHTBLACK_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_lightred(self):
        text1 = color("unittest lightred")
        text2 = color.lightred(text1)
        text1.foreground = Fore.LIGHTRED_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_lightgreen(self):
        text1 = color("unittest lightgreen")
        text2 = color.lightgreen(text1)
        text1.foreground = Fore.LIGHTGREEN_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_lightyellow(self):
        text1 = color("unittest lightyellow")
        text2 = color.lightyellow(text1)
        text1.foreground = Fore.LIGHTYELLOW_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_lightblue(self):
        text1 = color("unittest lightblue")
        text2 = color.lightblue(text1)
        text1.foreground = Fore.LIGHTBLUE_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_lightmagenta(self):
        text1 = color("unittest lightmagenta")
        text2 = color.lightmagenta(text1)
        text1.foreground = Fore.LIGHTMAGENTA_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_lightcyan(self):
        text1 = color("unittest lightcyan")
        text2 = color.lightcyan(text1)
        text1.foreground = Fore.LIGHTCYAN_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_lightwhite(self):
        text1 = color("unittest lightwhite")
        text2 = color.lightwhite(text1)
        text1.foreground = Fore.LIGHTWHITE_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_black(self):
        text1 = color("unittest black")
        text2 = color.back_black(text1)
        text1.background = Back.BLACK
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_red(self):
        text1 = color("unittest red")
        text2 = color.back_red(text1)
        text1.background = Back.RED
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_green(self):
        text1 = color("unittest green")
        text2 = color.back_green(text1)
        text1.background = Back.GREEN
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_yellow(self):
        text1 = color("unittest yellow")
        text2 = color.back_yellow(text1)
        text1.background = Back.YELLOW
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_blue(self):
        text1 = color("unittest blue")
        text2 = color.back_blue(text1)
        text1.background = Back.BLUE
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_magenta(self):
        text1 = color("unittest magenta")
        text2 = color.back_magenta(text1)
        text1.background = Back.MAGENTA
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_cyan(self):
        text1 = color("unittest cyan")
        text2 = color.back_cyan(text1)
        text1.background = Back.CYAN
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_white(self):
        text1 = color("unittest white")
        text2 = color.back_white(text1)
        text1.background = Back.WHITE
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_lightblack(self):
        text1 = color("unittest lightblack")
        text2 = color.back_lightblack(text1)
        text1.background = Back.LIGHTBLACK_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_lightred(self):
        text1 = color("unittest lightred")
        text2 = color.back_lightred(text1)
        text1.background = Back.LIGHTRED_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_lightgreen(self):
        text1 = color("unittest lightgreen")
        text2 = color.back_lightgreen(text1)
        text1.background = Back.LIGHTGREEN_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_lightyellow(self):
        text1 = color("unittest lightyellow")
        text2 = color.back_lightyellow(text1)
        text1.background = Back.LIGHTYELLOW_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_lightblue(self):
        text1 = color("unittest lightblue")
        text2 = color.back_lightblue(text1)
        text1.background = Back.LIGHTBLUE_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_lightmagenta(self):
        text1 = color("unittest lightmagenta")
        text2 = color.back_lightmagenta(text1)
        text1.background = Back.LIGHTMAGENTA_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_lightcyan(self):
        text1 = color("unittest lightcyan")
        text2 = color.back_lightcyan(text1)
        text1.background = Back.LIGHTCYAN_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))

    def test_back_lightwhite(self):
        text1 = color("unittest lightwhite")
        text2 = color.back_lightwhite(text1)
        text1.background = Back.LIGHTWHITE_EX
        commands().stdout(f"text1: {text1}")
        commands().stdout(f"text2: {text2}")
        self.assertEqual(str(text1), str(text2))


if __name__ == "__main__":
    unittest.main()
