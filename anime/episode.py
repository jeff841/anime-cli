from re import fullmatch
from argparse import ArgumentTypeError

def episode(value):
    if fullmatch(r'ep\d+',value):
        return value
    raise ArgumentTypeError('Episode must be in the format ep<number>')

