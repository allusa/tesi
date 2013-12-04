# -*- encoding: utf-8 -*-
"""
=====================================
Model estructural de sèries temporals
=====================================

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació del model estructural de Sèrie Temporal.
"""





class TimeSeriesStructure(set):
    """
    Sèrie temporal s = {m0,...,mk} com una seqüència de mesures ordenades en el temps

    És una subclasse de set. De la definició de set a Python:

     A set is an unordered collection with no duplicate elements.
     Basic uses include membership testing and eliminating duplicate entries. Set objects also support mathematical operations like union, intersection, difference, and symmetric difference.

    Un `set` és un conjunt d'elements no repetits però sense ordre. Els tipus amb ordre a Python s'anomenen `sequence` però no són conjunts.  Oficialment a Python (v2.7) no hi ha un `OrderedSet`.




    """
    """
    refer doctest com a TimeSeriesStructure
    >>> from measure import Measure
    >>> m1 = Measure(1,10)
    >>> m2 = Measure(2,10)
    >>> m3 = Measure(1,20)
    >>> s = SerieTemporal()
    >>> 
    >>> s.add(m1)
    >>> s.add(m2)
    >>> s.add(m3) #repetit, no s'afegeix
    >>> s
    SerieTemporal([m(1,10), m(2,10)])
    >>> min(s)
    m(1,10)
    >>> max(s)
    m(2,10)
    >>> s[2]
    m(2,10)
    >>>
    >>> m4 = Measure(5,40)
    >>> s.add(m4)
    >>> s[1:4]
    SerieTemporal([m(2,10)])
    >>> s[0:]
    SerieTemporal([m(1,10), m(2,10), m(5,40)])
    >>> 
    >>> s[1:4].issubset(s)
    True
    >>> s2 = SerieTemporal()
    >>> m5 = Measure(6,34)
    >>> s2.add(m4)
    >>> s2.add(m5)
    >>> s2.issubset(s)
    False
    >>> s.union(s2) # s | s2
    SerieTemporal([m(1,10), m(2,10), m(5,40), m(6,34)])
    >>> s.intersection(s2) # s & s2
    SerieTemporal([m(5,40)])
    >>> s.difference(s2) # s - s2
    SerieTemporal([m(1,10), m(2,10)])
    >>> s.symmetric_difference(s2) # s ^ s2
    SerieTemporal([m(1,10), m(2,10), m(6,34)])
    >>>
    >>> s.seg(m1)
    m(2,10)
    >>> s.ant(m2)
    m(1,10)
    """

    def t(self):
        """
        Vector temps
        """
        return set([m.t for m in self])




