# coding:utf-8

from typing import Optional
from typing import Set
from typing import Union

from colorama import Back
from colorama import Fore
from colorama.ansi import AnsiStyle
from colorama.ansi import code_to_chars


class AnsiXStyle(AnsiStyle):
    ITALIC = 3
    UNDERLINE = 4
    SLOWBLINK = 5
    RAPIDBLINK = 6
    INVERT = 7
    HIDE = 8
    STRIKETHROUGH = 9
    DOUBLYUNDERLINED = 21
    RESET_ITALIC = 23
    RESET_UNDERLINE = 24
    RESET_BLINK = 25
    RESET_INVERT = 27
    REVEAL = 28
    RESET_STRIKETHROUGH = 29


Style = AnsiXStyle()
StyleType = Union[str, int]
SytleReset = {
    Style.BRIGHT: Style.NORMAL,
    Style.DIM: Style.NORMAL,
    Style.ITALIC: Style.RESET_ITALIC,
    Style.UNDERLINE: Style.RESET_UNDERLINE,
    Style.SLOWBLINK: Style.RESET_BLINK,
    Style.RAPIDBLINK: Style.RESET_BLINK,
    Style.INVERT: Style.RESET_INVERT,
    Style.STRIKETHROUGH: Style.RESET_STRIKETHROUGH,
    Style.DOUBLYUNDERLINED: Style.RESET_UNDERLINE,
}


class color(str):
    '''Colorful terminal text

    Reference: https://en.wikipedia.org/wiki/ANSI_escape_code
    '''

    def __init__(self, object: object):
        self.__background: Optional[str] = None
        self.__foreground: Optional[str] = None
        self.__style: Set[str] = set()
        super().__init__()

    def __str__(self) -> str:
        message: str = super().__str__()

        if isinstance(self.foreground, str):
            message = f"{self.foreground}{message}{Fore.RESET}"

        if isinstance(self.background, str):
            message = f"{self.background}{message}{Back.RESET}"

        if len(self.style) > 0:
            for style in self.style:
                reset_style = SytleReset.get(style, Style.RESET_ALL)
                message = f"{style}{message}{reset_style}"
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
    def style(self, value: Set[StyleType]):
        assert isinstance(value, set), f"Unexpected type: {type(value)}"
        _value: Set[str] = {code_to_chars(v) if isinstance(v, int) else v
                            for v in value}
        self.__style = _value

    def add_style(self, value: StyleType) -> "color":
        assert isinstance(value, StyleType), f"Unexpected type: {type(value)}"
        _value: str = code_to_chars(value) if isinstance(value, int) else value
        self.__style.add(_value)
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
    def new_style(cls, object: object, value: Set[StyleType]) -> "color":
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
    def italic(cls, object: object) -> "color":
        return color.new_style(object, {Style.ITALIC})

    @classmethod
    def underline(cls, object: object) -> "color":
        return color.new_style(object, {Style.UNDERLINE})

    @classmethod
    def slow_blink(cls, object: object) -> "color":
        return color.new_style(object, {Style.SLOWBLINK})

    @classmethod
    def rapid_blink(cls, object: object) -> "color":
        return color.new_style(object, {Style.RAPIDBLINK})

    @classmethod
    def invert(cls, object: object) -> "color":
        return color.new_style(object, {Style.INVERT})

    @classmethod
    def hide(cls, object: object) -> "color":
        return color.new_style(object, {Style.HIDE})

    @classmethod
    def strikethrough(cls, object: object) -> "color":
        return color.new_style(object, {Style.STRIKETHROUGH})

    @classmethod
    def doubly_underlined(cls, object: object) -> "color":
        return color.new_style(object, {Style.DOUBLYUNDERLINED})

    @classmethod
    def normal(cls, object: object) -> "color":
        return color.new_style(object, {Style.NORMAL})

    @classmethod
    def reveal(cls, object: object) -> "color":
        return color.new_style(object, {Style.REVEAL})

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
    def black_back(cls, object: object) -> "color":
        return color.new_background(object, Back.BLACK)

    @classmethod
    def red_back(cls, object: object) -> "color":
        return color.new_background(object, Back.RED)

    @classmethod
    def green_back(cls, object: object) -> "color":
        return color.new_background(object, Back.GREEN)

    @classmethod
    def yellow_back(cls, object: object) -> "color":
        return color.new_background(object, Back.YELLOW)

    @classmethod
    def blue_back(cls, object: object) -> "color":
        return color.new_background(object, Back.BLUE)

    @classmethod
    def magenta_back(cls, object: object) -> "color":
        return color.new_background(object, Back.MAGENTA)

    @classmethod
    def cyan_back(cls, object: object) -> "color":
        return color.new_background(object, Back.CYAN)

    @classmethod
    def white_back(cls, object: object) -> "color":
        return color.new_background(object, Back.WHITE)

    @classmethod
    def lightblack_back(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTBLACK_EX)

    @classmethod
    def lightred_back(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTRED_EX)

    @classmethod
    def lightgreen_back(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTGREEN_EX)

    @classmethod
    def lightyellow_back(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTYELLOW_EX)

    @classmethod
    def lightblue_back(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTBLUE_EX)

    @classmethod
    def lightmagenta_back(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTMAGENTA_EX)

    @classmethod
    def lightcyan_back(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTCYAN_EX)

    @classmethod
    def lightwhite_back(cls, object: object) -> "color":
        return color.new_background(object, Back.LIGHTWHITE_EX)
