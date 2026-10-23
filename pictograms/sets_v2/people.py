"""Style 2 people (see kit2.py)."""
from kit2 import *


@picto('mom', 'mama', style=2)
def mom():
    return portrait('mom')


@picto('dad', 'otec', style=2)
def dad():
    return portrait('dad')


@picto('brother', 'brat', style=2)
def brother():
    return portrait('brother')


@picto('sister', 'sestra', style=2)
def sister():
    return portrait('sister')


@picto('grandma', 'babička', style=2)
def grandma():
    return portrait('grandma')


@picto('grandpa', 'dedko', style=2)
def grandpa():
    return portrait('grandpa')


@picto('happy', 'veselý', style=2)
def happy():
    return big_face('smile')


@picto('sad', 'smutný', style=2)
def sad():
    return big_face('sad')
