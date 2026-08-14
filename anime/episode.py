from re import fullmatch
from argparse import ArgumentTypeError
from .constants import EPISODE_ERROR

def episode(value):
    if fullmatch(r'ep\d+',value):
        return value
    raise ArgumentTypeError(EPISODE_ERROR)

