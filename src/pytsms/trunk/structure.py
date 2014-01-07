# -*- encoding: utf-8 -*-
"""
=====================================
Model estructural de sèries temporals
=====================================

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació del model estructural de Sèrie Temporal.
"""

from measure import Measure



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
    def sup(self):
        """
        Suprem de la sèrie temporal

        :return: `sup(S)`, la mesura suprema de S
        :rtype: :class:`measure.Measure`

        >>> s = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s.sup() == Measure(3,2)
        True
        >>> s2 = TimeSeriesStructure([])
        >>> s2.sup().isundefinedn()
        True
        """
        if len(self) == 0:
            return Measure(-float("inf"),float("inf")) #S'hauria de fer independent del tipus de valor
        else:
            return max(self)


    def inf(self):
        """
        Ínfim de la sèrie temporal

        :returns: `inf(S)`, la mesura ínfima de S
        :rtype: :class:`measure.Measure`

        >>> s = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s.inf() == Measure(1,2)
        True
        >>> s2 = TimeSeriesStructure([])
        >>> s2.inf().isundefinedp()
        True
        """
        if len(self) == 0:
            return Measure(+float("inf"),float("inf"))
        else:
            return min(self)


    #ALTRES


    def t(self):
        """
        Vector temps
        """
        return set([m.t for m in self])


    def empty(self):
        """
        Retorna una sèrie temporal buida del mateix tipus i amb els
        mateixos atributs
        """
        s = type(self)()
        s.set_rpr(self.get_rpr())
        return s

    def copy(self):
        """
        Sobrecàrrega del mètode copy
        Retorna una còpia de la sèrie temporal amb els
        mateixos atributs        
        """
        s = set.copy(self)
        s.set_rpr(self.get_rpr())
        return s    


    def set_rpr(self,rpr):
        """
        Permet definir una representació per defecte de la sèrie
        temporal. S'aplicarà per defecte a tots els operadors de
        funció temporal.

        :param rpr: Una representació per a la sèrie temporal
        :type rpr: :class:`representation.Representation`
        """        
        self._rpr = rpr


    def get_rpr(self):
        """
        Permet obtenir la representació per defecte de la sèrie
        temporal.

        :return: El tipus de representació per a la sèrie temporal
        :rtype: :class:`representation.Representation` or None
        """        
        try:
            return self._rpr
        except AttributeError:
            return None
