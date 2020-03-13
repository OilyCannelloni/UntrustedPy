"""
This file contains some numerical constants
"""


class Keys:
    """
    PyGame arrow key id's
    """
    UP = 273
    DOWN = 274
    RIGHT = 275
    LEFT = 276


class Colors:
    """
    RGB colors
    """
    BLACK = (0, 0, 0)
    D_GRAY = (10, 10, 10)
    MD_GRAY = (30, 30, 30)
    WHITE = (255, 255, 255)
    ORANGE = (255, 100, 0)
    MAGENTA = (255, 0, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    AQUA = (0, 255, 255)
    NAVY = (0, 0, 56)
    SCARLET = (255, 51, 0)


class Events:
    """
    Custom PyGame Events
    """
    LEVEL = 25
    CONSOLE_TOGGLE = 26


class Type:
    """
    Object types
    """
    STATIC = 0
    DYNAMIC = 1
    PLAYER = 2
