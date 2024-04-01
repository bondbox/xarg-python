# coding:utf-8

from xarg import Style
from xarg import color

COLOUR = color(f"{color.red(123)}{color.yellow(456)}{color.green(789)}")
print(f"{COLOUR}: COLORFUL")

COLOUR.style = {Style.INVERT}
print(f"{COLOUR}: COLORFUL and INVERT")

COLOUR.style = {Style.UNDERLINE}
print(f"{COLOUR}: COLORFUL and UNDERLINE")

COLOUR.style = {Style.STRIKETHROUGH}
print(f"{COLOUR}: COLORFUL and STRIKETHROUGH")

COLOUR.style = {Style.INVERT, Style.UNDERLINE}
print(f"{COLOUR}: COLORFUL and INVERT and UNDERLINE")

COLOUR.style = {Style.INVERT, Style.STRIKETHROUGH}
print(f"{COLOUR}: COLORFUL and INVERT and STRIKETHROUGH")

COLOUR.style = {Style.UNDERLINE, Style.STRIKETHROUGH}
print(f"{COLOUR}: COLORFUL and UNDERLINE and STRIKETHROUGH")

COLOUR.style = {Style.INVERT, Style.UNDERLINE, Style.STRIKETHROUGH}
print(f"{COLOUR}: COLORFUL and INVERT and UNDERLINE and STRIKETHROUGH")
