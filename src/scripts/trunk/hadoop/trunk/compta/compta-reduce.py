#!/usr/bin/env python

"""
Hadoop reduce function for word counter

input (hadoop sorts keys): 
feu 1
hola 1
hola 1
que 1
que 1
tal 1


output:
feu 1
hola 2
que 2
tal 1
"""


import sys


def agrupa_llista(f):
    """
    >>> s = "feu\\t1\\nhola\\t1\\nhola\\t1\\nque\\t1\\nque\\t1\\ntal\\t1"
    >>> agrupa_llista(s.split('\\n'))  # doctest: +NORMALIZE_WHITESPACE
    feu 1
    hola 2
    que 2
    tal 1
    """
    word = None
    count = 0

    for line in f:
        line = line.rstrip()
        wc = line.split()
        if len(wc) != 2:
            w = None
            c = 0
        else:
            w,c = wc
            c = int(c)

        if word == w:
            count += int(c)
        else:
            if word is not None:
                print '{0}\t{1}'.format(word,count)
            word = w
            count = c
        
    if word is not None:
        print '{0}\t{1}'.format(word,count)      




if __name__ == '__main__':
    agrupa_llista(sys.stdin)



#test: cat compta-map.py | python compta-map.py | sort -k1,1 | python compta-reduce.py
