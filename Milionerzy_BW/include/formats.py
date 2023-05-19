from collections import namedtuple
from PyQt5.QtGui import QFont

colors = namedtuple('colors', ['gray', 'yellow', 'green', 'red', 'black'])
fonts = namedtuple('fonts', ['Qfont'])

BACKGROUND_COLORS = colors(
    gray="background-color:#fff;",
    yellow="background-color:#ff0;",
    green="background-color:#0f0;",
    red="background-color:#f00;",
    black="background-color:#000;"
)

q_font = QFont('Arial', 18)
q_font.setBold(True)

FONTS = fonts(
    Qfont=q_font
)
