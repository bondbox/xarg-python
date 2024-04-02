# coding:utf-8

from typing import Optional
from typing import Set

from colorama import Back
from colorama import Fore
from colorama import Style


class color(str):
    '''Colorful terminal text

    Reference: https://en.wikipedia.org/wiki/ANSI_escape_code
    '''

    def __init__(self, object: object):
        self.__background: Optional[str] = None
        self.__foreground: Optional[str] = None
        self.__style: Set[str] = set()
        self.__reset: bool = True
        super().__init__()

    def __str__(self) -> str:
        message: str = super().__str__()

        if isinstance(self.foreground, str):
            message = f"{self.foreground}{message}{Fore.RESET}"

        if isinstance(self.background, str):
            message = f"{self.background}{message}{Back.RESET}"

        if len(self.style) > 0:
            for style in self.style:
                message = f"{style}{message}"
            if self.reset:
                message = f"{message}{Style.RESET_ALL}"
        return message

    @property
    def background(self) -> Optional[str]:
        return self.__background

    @background.setter
    def background(self, value: str):
        assert isinstance(value, str), f"Unexpected type: {type(value)}"
        self.__background = value

    @property
    def foreground(self) -> Optional[str]:
        return self.__foreground

    @foreground.setter
    def foreground(self, value: str):
        assert isinstance(value, str), f"Unexpected type: {type(value)}"
        self.__foreground = value

    @property
    def style(self) -> Set[str]:
        return self.__style

    @style.setter
    def style(self, value: Set[str]):
        assert isinstance(value, set), f"Unexpected type: {type(value)}"
        self.__style = value

    @property
    def reset_style(self) -> bool:
        return self.__reset

    @reset_style.setter
    def reset_style(self, value: bool):
        assert isinstance(value, bool), f"Unexpected type: {type(value)}"
        self.__reset = value

    def add_style(self, value: str):
        assert isinstance(value, str), f"Unexpected type: {type(value)}"
        self.__style.add(value)

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
    def new_style(cls, object: object, value: Set[str]) -> "color":
        colour: color = color(object)
        colour.style = value
        return colour

    @classmethod
    def reset(cls) -> str:
        return Style.RESET_ALL

    @classmethod
    def bold(cls, object: object) -> "color":
        return color.new_style(object, {Style.BRIGHT})

    @classmethod
    def dim(cls, object: object) -> "color":
        return color.new_style(object, {Style.DIM})

    @classmethod
    def normal(cls, object: object) -> "color":
        return color.new_style(object, {Style.NORMAL})

    @classmethod
    def black(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.BLACK)

    @classmethod
    def red(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.RED)

    @classmethod
    def green(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.GREEN)

    @classmethod
    def yellow(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.YELLOW)

    @classmethod
    def blue(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.BLUE)

    @classmethod
    def magenta(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.MAGENTA)

    @classmethod
    def cyan(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.CYAN)

    @classmethod
    def white(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.WHITE)

    @classmethod
    def lightblack(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.LIGHTBLACK_EX)

    @classmethod
    def lightred(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.LIGHTRED_EX)

    @classmethod
    def lightgreen(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.LIGHTGREEN_EX)

    @classmethod
    def lightyellow(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.LIGHTYELLOW_EX)

    @classmethod
    def lightblue(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.LIGHTBLUE_EX)

    @classmethod
    def lightmagenta(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.LIGHTMAGENTA_EX)

    @classmethod
    def lightcyan(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.LIGHTCYAN_EX)

    @classmethod
    def lightwhite(cls, object: object) -> "color":
        return color.new_foreground(object, Fore.LIGHTWHITE_EX)

    @classmethod
    def back_black(cls, object: object) -> "color":
        return color.new_background(object, Back.BLACK)

    @classmethod
    def back_red(cls, object: object) -> "color":
        return color.new_background(object, Back.RED)

    @classmethod
    def back_green(cls, object: object) -> "color":
        return color.new_background(object, Back.GREEN)

    @classmethod
    def back_yellow(cls, object: object) -> "color":
        return color.new_background(object, Back.YELLOW)

    @classmethod
    def back_blue(cls, object: object) -> "color":
        return color.new_background(object, Back.BLUE)

    @classmethod
    def back_magenta(cls, object: object) -> "color":
        return color.new_background(object, Back.MAGENTA)

    @classmethod
    def back_cyan(cls, object: object) -> "color":
        return color.new_background(object, Back.CYAN)

    @classmethod
    def back_white(cls, object: object) -> "color":
        return color.new_background(object, Back.WHITE)

    @classmethod
    def back_lightblack(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTBLACK_EX)

    @classmethod
    def back_lightred(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTRED_EX)

    @classmethod
    def back_lightgreen(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTGREEN_EX)

    @classmethod
    def back_lightyellow(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTYELLOW_EX)

    @classmethod
    def back_lightblue(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTBLUE_EX)

    @classmethod
    def back_lightmagenta(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTMAGENTA_EX)

    @classmethod
    def back_lightcyan(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTCYAN_EX)

    @classmethod
    def back_lightwhite(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTWHITE_EX)
