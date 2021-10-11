import math

from disnake import SelectOption, ButtonStyle
from disnake.ui import View, Select, Button

buttons = [
    [
        Button(style=ButtonStyle.grey, label="1"),
        Button(style=ButtonStyle.grey, label="2"),
        Button(style=ButtonStyle.grey, label="3"),
        Button(style=ButtonStyle.green, label="×"),
        Button(style=ButtonStyle.red, label="Exit"),
    ],
    [
        Button(style=ButtonStyle.grey, label="4"),
        Button(style=ButtonStyle.grey, label="5"),
        Button(style=ButtonStyle.grey, label="6"),
        Button(style=ButtonStyle.green, label="÷"),
        Button(style=ButtonStyle.red, label="←"),
    ],
    [
        Button(style=ButtonStyle.grey, label="7"),
        Button(style=ButtonStyle.grey, label="8"),
        Button(style=ButtonStyle.grey, label="9"),
        Button(style=ButtonStyle.green, label="+"),
        Button(style=ButtonStyle.red, label="Clear"),
    ],
    [
        Button(style=ButtonStyle.grey, label="00"),
        Button(style=ButtonStyle.grey, label="0"),
        Button(style=ButtonStyle.grey, label="."),
        Button(style=ButtonStyle.green, label="-"),
        Button(style=ButtonStyle.green, label="="),
    ],
    [
        Button(style=ButtonStyle.grey, label="("),
        Button(style=ButtonStyle.grey, label=")"),
        Button(style=ButtonStyle.grey, label="π"),
        # Button(style=ButtonStyle.grey, label="x²"),
        # Button(style=ButtonStyle.grey, label="x³"),
    ],
]


def calculate(exp):
    o = exp.replace("×", "*")
    o = o.replace("÷", "/")
    o = o.replace("π", str(math.pi))
    # o = o.replace("²", "**2")
    # o = o.replace("³", "**3")
    result = ""
    try:
        result = str(eval(o))

    except BaseException:
        result = "An error occurred."

    return result
