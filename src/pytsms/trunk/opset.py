# -*- encoding: utf-8 -*-

"""
============================================
Operadors de conjunts per a sèries temporals
============================================

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació dels operadors de conjunts de Sèrie Temporal.
"""


from measure import Measure
from structure import TimeSeriesStructure


# http://docs.python.org/2/reference/datamodel.html#special-method-lookup-for-old-style-classes
# http://docs.python.org/3.3/library/stdtypes.html#set
# http://en.wikipedia.org/wiki/Mathematical_operators_and_symbols_in_Unicode
  

#'isdisjoint', 'issubset', 'issuperset'

class TimeSeriesSetOpNoTemporal(TimeSeriesStructure):
    """
    Operadors de conjunts no temporals de Sèrie Temporal
    """

    def membership(self,m):
        """
        Operador de pertinença. Cert quan la mesura `m` pertany a la sèrie
        temporal.

        :param m: 
        :type m: :class:`Measure`
        :returns: `m ∈ s`, m pertany a s
        :rtype: bool

        >>> s = TimeSeriesSetOp([Measure(1,2)])
        >>> m1 = Measure(1,2)
        >>> m2 = Measure(1,1)
        >>> s.membership(m1)
        True
        >>> s.membership(m2)
        False
        """
        for ms in self:
            if m.eqnt(ms):
                return True
        return False

    def subset(self,s):
        """
        Operador de subconjunt. Cert quan la sèrie temporal està
        inclosa a la sèrie temporal `s`.

        :param s: 
        :type s: :class:`TimeSeries`
        :returns: `s1 ⊆ s2`, s1 inclosa a s2
        :rtype: bool

        >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
        >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,1)])
        >>> s3 = TimeSeriesSetOp([Measure(1,5)])
        >>> s1.subset(s2)
        True
        >>> s2.subset(s1)
        False
        >>> s3.subset(s1)
        False
        >>> s1.subset(s3)
        False
        """
        for m1 in self:
            if not s.membership(m1):
                return False
        return True

    def union(self, other):
        """
        Operador d'unió. Sèrie temporal resultant d'unir la sèrie
        temporal amb `other`.

        :param other: 
        :type other: :class:`TimeSeries`
        :returns: `s1 ∪ s2`, s1 unió s2
        :rtype: :class:`TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
        >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s2.union(s1) == s2
        True
        >>> s1.union(s2) == TimeSeriesSetOp([Measure(1,2), Measure(3,2), Measure(2,1)])
        True
        """
        s = self.copy()
        for m2 in other:
            if not s.membership_temporal(m2):
                s.add(m2)
        return s

    def difference(self, other):
        """
        Operador de diferència Sèrie temporal resultant de treure
        `other de la sèrie temporal.

        :param other: 
        :type other: :class:`TimeSeries`
        :returns: `s1 - s2`, s1 diferència s2
        :rtype: :class:`TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
        >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s1.difference(s1) == TimeSeriesSetOp([])
        True
        >>> s1.difference(s2) == TimeSeriesSetOp([Measure(2,1)])
        True
        >>> s2.difference(s1) == TimeSeriesSetOp([Measure(2,2),Measure(3,2)])
        True
        """
        s = type(self)()
        for m1 in self:
            if not other.membership(m1):
                s.add(m1)
        return s

    def intersection(self, other):
        """
        Operador d'intersecció. Sèrie temporal resultant
        d'interseccionar `other amb la sèrie temporal.

        :param other: 
        :type other: :class:`TimeSeries`
        :returns: `s1 ∩ s2`, s1 intersecció s2
        :rtype: :class:`TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
        >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s1.intersection(s1) == s1
        True
        >>> s1.intersection(s2) == TimeSeriesSetOp([Measure(1,2)])
        True
        >>> s2.intersection(s1) == s1.intersection(s2)
        True
        """
        return self.difference(self.difference(other))


    def symmetric_difference(self, other):
        """
        Operador de diferència simètrica. Sèrie temporal resultant
        de la diferènca simètrica d'`other amb la sèrie temporal.

        :param other: 
        :type other: :class:`TimeSeries`
        :returns: `s1 ⊖ s2`, s1 diferència simètrica s2
        :rtype: :class:`TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
        >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s1.symmetric_difference(s1) == TimeSeriesSetOp([])
        True
        >>> s1.symmetric_difference(s2) == TimeSeriesSetOp([Measure(2,1),Measure(3,2)])
        True
        >>> s2.symmetric_difference(s1) == TimeSeriesSetOp([Measure(2,2),Measure(3,2)])
        True
        """
        return self.difference(other).union(other.difference(self))




class TimeSeriesSetOpTemporal(TimeSeriesStructure):
    """
    Operadors de conjunts temporals de Sèrie Temporal
    """


    def membership_temporal(self,m):
        """
        Operador de pertinença temporal. Cert quan la mesura `m` pertany
        temporalment a la sèrie temporal.

        Cerca si m.t pertany al conjunt de temps de s (s.t())
        Sempre es compleix que si membership(m,S)==True aleshores
        membership_temporal(m,S)==True

        :param m: 
        :type m: :class:`Measure`
        :returns: `m ∈ᵗ s`, m pertany temporalment a s
        :rtype: bool

        >>> s = TimeSeriesSetOp([Measure(1,2)])
        >>> m1 = Measure(1,2)
        >>> m2 = Measure(1,1)
        >>> s.membership_temporal(m1)
        True
        >>> s.membership_temporal(m2)
        True
        >>> s.membership_temporal(Measure(2,2))
        False
        """
        return m.t in self.t()


    def subset_temporal(self,s):
        """
        Operador de subconjunt temporal. Cert quan la sèrie temporal està
        inclosa temporalment a la sèrie temporal `s`.

        Sempre es compleix que si s1.subset(s2)==True aleshores
        s1.subset_temporal(s2)==True

        :param s: 
        :type s: :class:`TimeSeries`
        :returns: `s1 ⊆ᵗ s2`, s1 inclosa temporalment a s2
        :rtype: bool

        >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
        >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,1)])
        >>> s3 = TimeSeriesSetOp([Measure(1,5)])
        >>> s1.subset_temporal(s2)
        True
        >>> s2.subset_temporal(s1)
        False
        >>> s1.subset_temporal(s3)
        False
        >>> s3.subset_temporal(s1)
        True
        """
        for m1 in self:
            if not s.membership_temporal(m1):
                return False
        return True


    def union_temporal(self, other):
        """
        Operador d'unió temporal. Sèrie temporal resultant d'unir
        temporalment la sèries temporals amb `other`.

        :param other: 
        :type other: :class:`TimeSeries`
        :returns: `s1 ∪ᵗ s2`, s1 unió temporal s2
        :rtype: :class:`TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
        >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s2.union_temporal(s1) ==  TimeSeriesSetOp([Measure(3,2),Measure(1,2),])
        True
        >>> s1.union_temporal(s2) == s2.union_temporal(s1)
        True
        """
        s = type(self)()
        for m1 in self:
            if not other.membership_temporal(m1):
                s.add(m1)
            elif other.membership(m1):
                s.add(m1)

        for m2 in other:
            if not self.membership_temporal(m2):
                s.add(m2)
        return s

    def difference_temporal(self, other):
        """
        Operador de diferència temporal. Sèrie temporal resultant de
        treure temporalment `other de la sèrie temporal.

        :param other: 
        :type other: :class:`TimeSeries`
        :returns: `s1 -ᵗ s2`, s1 diferència temporal s2
        :rtype: :class:`TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
        >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s1.difference_temporal(s1) == s1.difference(s1)
        True
        >>> s1.difference_temporal(s2) == TimeSeriesSetOp([])
        True
        >>> s2.difference_temporal(s1) == TimeSeriesSetOp([Measure(3,2)])
        True
        """
        s = type(self)()
        for m1 in self:
            if not other.membership_temporal(m1):
                s.add(m1)
        return s

    def intersection_temporal(self, other):
        """
        Operador d'intersecció temporal. Sèrie temporal resultant
        d'interseccionar temporalment `other amb la sèrie temporal.

        :param other: 
        :type other: :class:`TimeSeries`
        :returns: `s1 ∩ᵗ s2`, s1 intersecció temporal s2
        :rtype: :class:`TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
        >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s1.intersection_temporal(s1) == s1.intersection(s1)
        True
        >>> s1.intersection_temporal(s2) == TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
        True
        >>> s2.intersection_temporal(s1) == TimeSeriesSetOp([Measure(1,2),Measure(2,2)])
        True
        """
        return self.difference_temporal(self.difference_temporal(other))


    def symmetric_difference_temporal(self, other):
        """
        Operador de diferència simètrica temporal. Sèrie temporal resultant
        de la diferènca simètrica temporal d'`other amb la sèrie temporal.

        :param other: 
        :type other: :class:`TimeSeries`
        :returns: `s1 ⊖ᵗ s2`, s1 diferència simètrica temporal s2
        :rtype: :class:`TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
        >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s1.symmetric_difference_temporal(s1) == s1.symmetric_difference(s1)
        True
        >>> s1.symmetric_difference_temporal(s2) == TimeSeriesSetOp([Measure(3,2)])
        True
        >>> s2.symmetric_difference_temporal(s1) == s1.symmetric_difference_temporal(s2)
        True
        """
        return self.difference_temporal(other).union_temporal(other.difference_temporal(self))




class TimeSeriesSetOpRelacional(TimeSeriesStructure):
    """
    Operadors de conjunts relacionals de Sèrie Temporal
    """

    def projection(self,A):
        """
        Operador de projecció. Conjunt resultant de seleccionar
        els atributs (columnes) `A` de la sèrie temporal.

        :param A: exemple ['t','v']
        :type A: Iterable of attribute names
        :returns: `s{A}`, projecció de s en A
        :rtype: set

        >>> s1 = TimeSeriesSetOp([Measure(1,1),Measure(2,1)])
        >>> TimeSeriesSetOp([]).projection([]) == set()
        True
        >>> s1.projection([])  == set([])
        True
        >>> s1.projection(['t']) == set([1,2])
        True
        >>> s1.projection(['v']) == set([1])
        True
        >>> s1.projection(['t','v']) == set([(1,1),(2,1)])
        True
        """
        s = set()       
        for m in self:
            row = []
            for a in A:              
                if a == 't':
                    row.append(m.t)
                if a == 'v':
                    row.append(m.v)

            if len(row) > 1:
                s.add(tuple(row))
            elif len(row) == 1:
                s.add(row[0])
            else:
                pass
        return s








class TimeSeriesSetOp( TimeSeriesSetOpRelacional,TimeSeriesSetOpNoTemporal,TimeSeriesSetOpTemporal):
    """
    Operadors de conjunts de Sèrie Temporal, inclou els Temporals i
    els no Temporals.

    >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> s1 | s2 == s1.union(s2)
    True
    >>> s2 | s1 == s2.union(s1)
    True
    """
    def __or__(self, other):
        """
        Binary arithmetic operation union for sets, symbol `|`.
        """
        return self.union(other)



















