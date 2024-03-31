# coding:utf-8

from typing import List
from typing import Optional

from colorama import Back
from colorama import Fore
from colorama import Style


class color(str):
    '''
    Reference: https://en.wikipedia.org/wiki/ANSI_escape_code
    '''

    def __init__(self, object: object):
        self.__background: Optional[str] = None
        self.__foreground: Optional[str] = None
        super().__init__()

    def __str__(self) -> str:
        fore_back = [self.foreground, self.background]
        items: List[str] = [i for i in fore_back if isinstance(i, str)]
        if len(items) <= 0:
            return self
        items.extend([self, Style.RESET_ALL])
        return "".join(items)

    @property
    def background(self) -> Optional[str]:
        return self.__background

    @background.setter
    def background(self, value: str):
        assert isinstance(value, str), f"Unexpected type: {type(value)}"
        self.__background = value
        return self

    @property
    def foreground(self) -> Optional[str]:
        return self.__foreground

    @foreground.setter
    def foreground(self, value: str):
        assert isinstance(value, str), f"Unexpected type: {type(value)}"
        self.__foreground = value
        return self

    @classmethod
    def new_background(cls, object: object, value: str) -> "color":
        colour: color = color(object)
        colour.background = value
        return colour

    @classmethod
    def new_foreground(cls, object: object, value: str) -> "color":
        colour: color = color(object)
        colour.foreground = value
        return colour

    @classmethod
    def black(cls, object: object):
        return color.new_foreground(object, Fore.BLACK)

    @classmethod
    def red(cls, object: object):
        return color.new_foreground(object, Fore.RED)

    @classmethod
    def green(cls, object: object):
        return color.new_foreground(object, Fore.GREEN)

    @classmethod
    def yellow(cls, object: object):
        return color.new_foreground(object, Fore.YELLOW)

    @classmethod
    def blue(cls, object: object) -> str:
        return color.new_foreground(object, Fore.BLUE)

    @classmethod
    def magenta(cls, object: object) -> str:
        return color.new_foreground(object, Fore.MAGENTA)

    @classmethod
    def cyan(cls, object: object) -> str:
        return color.new_foreground(object, Fore.CYAN)

    @classmethod
    def white(cls, object: object) -> str:
        return color.new_foreground(object, Fore.WHITE)

    @classmethod
    def lightblack(cls, object: object):
        return color.new_foreground(object, Fore.LIGHTBLACK_EX)

    @classmethod
    def lightred(cls, object: object) -> str:
        return color.new_foreground(object, Fore.LIGHTRED_EX)

    @classmethod
    def lightgreen(cls, object: object):
        return color.new_foreground(object, Fore.LIGHTGREEN_EX)

    @classmethod
    def lightyellow(cls, object: object):
        return color.new_foreground(object, Fore.LIGHTYELLOW_EX)

    @classmethod
    def lightblue(cls, object: object) -> str:
        return color.new_foreground(object, Fore.LIGHTBLUE_EX)

    @classmethod
    def lightmagenta(cls, object: object) -> str:
        return color.new_foreground(object, Fore.LIGHTMAGENTA_EX)

    @classmethod
    def lightcyan(cls, object: object) -> str:
        return color.new_foreground(object, Fore.LIGHTCYAN_EX)

    @classmethod
    def lightwhite(cls, object: object) -> str:
        return color.new_foreground(object, Fore.LIGHTWHITE_EX)

    @classmethod
    def back_black(cls, object: object) -> str:
        return color.new_background(object, Back.BLACK)

    @classmethod
    def back_red(cls, object: object) -> str:
        return color.new_background(object, Back.RED)

    @classmethod
    def back_green(cls, object: object):
        return color.new_background(object, Back.GREEN)

    @classmethod
    def back_yellow(cls, object: object):
        return color.new_background(object, Back.YELLOW)

    @classmethod
    def back_blue(cls, object: object) -> str:
        return color.new_background(object, Back.BLUE)

    @classmethod
    def back_magenta(cls, object: object) -> str:
        return color.new_background(object, Back.MAGENTA)

    @classmethod
    def back_cyan(cls, object: object) -> str:
        return color.new_background(object, Back.CYAN)

    @classmethod
    def back_white(cls, object: object) -> str:
        return color.new_background(object, Back.WHITE)

    @classmethod
    def back_lightblack(cls, object: object):
        return color.new_background(object, Back.LIGHTBLACK_EX)

    @classmethod
    def back_lightred(cls, object: object) -> str:
        return color.new_background(object, Back.LIGHTRED_EX)

    @classmethod
    def back_lightgreen(cls, object: object):
        return color.new_background(object, Back.LIGHTGREEN_EX)

    @classmethod
    def back_lightyellow(cls, object: object):
        return color.new_background(object, Back.LIGHTYELLOW_EX)

    @classmethod
    def back_lightblue(cls, object: object) -> str:
        return color.new_background(object, Back.LIGHTBLUE_EX)

    @classmethod
    def back_lightmagenta(cls, object: object) -> str:
        return color.new_background(object, Back.LIGHTMAGENTA_EX)

    @classmethod
    def back_lightcyan(cls, object: object) -> str:
        return color.new_background(object, Back.LIGHTCYAN_EX)

    @classmethod
    def back_lightwhite(cls, object: object) -> str:
        return color.new_background(object, Back.LIGHTWHITE_EX)
