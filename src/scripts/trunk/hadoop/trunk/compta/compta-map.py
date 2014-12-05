#!/usr/bin/env python

"""
Hadoop map function for word counter

input: "hola que tal, hola que feu?"
output: 
hola 1
que 1
tal 1
hola 1
que 1
feu 1
"""


import sys


def compta_linia(l):
    """

    >>> compta_linia("hola")  # doctest: +NORMALIZE_WHITESPACE
    hola\t1
    >>> compta_linia("hola que tal, hola que feu?")  # doctest: +NORMALIZE_WHITESPACE
    hola\t1
    que\t1
    tal,\t1
    hola\t1
    que\t1
    feu?\t1
    """
    l = l.rstrip()
    for w in l.split():
        print "{0}\t1".format(w)


def compta_file(f):
    """

    >>> s="hola que tal,\\nhola que feu?"
    >>> compta_file(s.split("\\n")) # doctest: +NORMALIZE_WHITESPACE
    hola 1
    que 1
    tal, 1
    hola 1
    que 1
    feu? 1
    """
    for line in f:
        compta_linia(line)



if __name__ == '__main__':
    compta_file(sys.stdin)



# test: cat compta-map.py | python compta-map.py
