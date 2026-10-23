"""Style 2 people (see kit2.py). Sample set, more follows after the owner approves the look."""
from kit2 import *


@picto('mom', 'mama', style=2)
def mom():
    return figure('mom')


@picto('dad', 'otec', style=2)
def dad():
    return figure('dad')


@picto('brother', 'brat', style=2)
def brother():
    return figure('brother')


@picto('sister', 'sestra', style=2)
def sister():
    return figure('sister')


@picto('grandma', 'babička', style=2)
def grandma():
    return figure('grandma')


@picto('grandpa', 'dedko', style=2)
def grandpa():
    return figure('grandpa')


@picto('happy', 'veselý', style=2)
def happy():
    return emotion_face('smile')


@picto('sad', 'smutný', style=2)
def sad():
    return emotion_face('sad')
