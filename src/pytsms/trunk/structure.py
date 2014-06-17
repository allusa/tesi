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


    >>> from measure import Measure
    >>> m1 = Measure(1,10)
    >>> m2 = Measure(2,10)
    >>> m3 = Measure(1,20)
    >>> s = TimeSeriesStructure()
    >>> 
    >>> s.add(m1)
    >>> s.add(m2)
    >>> s.add(m3) #repetit, no s'afegeix
    >>> s
    TimeSeriesStructure([m(1,10), m(2,10)])
    >>>
    >>> s == s
    True
    >>> s ==  TimeSeriesStructure([Measure(1,10),Measure(2,10)])
    True
    >>> s ==  TimeSeriesStructure([Measure(1,10),Measure(2,20)])
    False
    >>> min(s)
    m(1,10)
    >>> max(s)
    m(2,10)
    >>>
    >>> m4 = Measure(5,40)
    >>> s.add(m4)
    >>> 
    >>> TimeSeriesStructure([m1,m2]).issubset(s)
    True
    >>> s2 = TimeSeriesStructure()
    >>> m5 = Measure(6,34)
    >>> s2.add(m4)
    >>> s2.add(m5)
    >>> s2.issubset(s)
    False
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
            return Measure(un='-')
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
            return Measure(un='+')
        else:
            return min(self)


    #ALTRES

    

    def t(self):
        """
        Vector temps
        """
        return set([m.t for m in self])


    def add(self,m):
        """
        Sobrecàrrega del mètode add per tal que s'utilitzi la igualtat eqt() entre mesures i puguem ser independents de com es defineixi el mètode __eq__() de les mesures.

        >>> from measure import Measure
        >>> m1 = Measure(1,10)
        >>> m2 = Measure(2,10)
        >>> m3 = Measure(1,20)
        >>> s = TimeSeriesStructure()
        >>> 
        >>> s.add(m1)
        >>> s.add(m2)
        >>> s.add(m3) #repetit, no s'afegeix
        >>> s
        TimeSeriesStructure([m(1,10), m(2,10)])
        """
        if m.t in self.t():
            return
        set.add(self,m)


    def copy(self):
        """
        Redefinició del mètode copy per tal que copiï també els atributs

        >>>
        >>> #SET predefined methods
        >>> #COPY
        >>> from timeseries import TimeSeries
        >>> s1 = TimeSeries([Measure(1,2)])
        >>> class AnyRpr(): pass
        >>> s1.set_rpr(AnyRpr)
        >>> s2 = s1.copy()
        >>> s1 is s2
        False
        >>> s1 == s2
        True
        >>> s2.get_rpr() == AnyRpr
        True
        >>> m1 = s1.pop()
        >>> m2 = s2.pop()
        >>> m1 is m2
        True
        >>> m1 == m2
        True
        """
        s = set.copy(self)
        s.__dict__.update(self.__dict__)
        return s

    def empty(self):
        """
        Retorna una sèrie temporal buida del mateix tipus i amb els
        mateixos atributs

        >>> from timeseries import TimeSeries
        >>> class AnyRpr(): pass
        >>> s = TimeSeries([Measure(1,2)])
        >>> s.set_rpr(AnyRpr)
        >>> s2 = s.empty()
        >>> s2 == TimeSeries([])
        True
        >>> s2.get_rpr() == AnyRpr
        True
        >>> #Predefined clear() is like empty but updates
        >>> s.clear()
        >>> s == TimeSeries([])
        True
        >>> s.get_rpr() == AnyRpr
        True
        """
        s = type(self)()
        s.__dict__.update(self.__dict__)
        return s


    def mtype(self):
        """
        Retorna el tipus de les mesures de la sèrie temporal. Cal pensar que una sèrie temporal és homogènia. QUÈ PASSA QUAN  LA SÈRIE TEMPORAL ÉS BUIDA?
        """
        if len(self) == 0:
            return Measure
        return type(next(iter(self)))





