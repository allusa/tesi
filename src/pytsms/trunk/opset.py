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
  

class TimeSeriesSetOp(TimeSeriesStructure):
    """
    Operadors de conjunts de Sèrie Temporal
    """

    def __or__(self, other):
        """
        Binary arithmetic operation union for sets, symbol `|`.
        """
        return union(self,other)






    def union(self, other):
        """
        Binary arithmetic operation union for sets, symbol `|`.
        """
        return union(self,other)

    def union_temporal(self, other):
        """
        Binary arithmetic operation temporal union for sets, symbol `|`.
        """
        return union_temporal(self,other)



class TimeSeriesSetOpTemporal(object):
    """
    Operadors de conjunts temporals de Sèrie Temporal
    """

    def __or__(self, other):
        """
        Binary arithmetic operation union for sets, symbol `|`.
        """
        return union_temporal(self,other)







def membership(m,s):
    """
    Operador de pertinença. Cert quan la mesura `m` pertany a la sèrie
    temporal `s`.

    :param m: 
    :type m: :class:`Measure`
    :param s: 
    :type s: :class:`TimeSeries`
    :returns: `m ∈ s`, m pertany a s
    :rtype: bool

    >>> s = TimeSeriesSetOp([Measure(1,2)])
    >>> m1 = Measure(1,2)
    >>> m2 = Measure(1,1)
    >>> membership(m1,s)
    True
    >>> membership(m2,s)
    False
    """
    for ms in s:
        if m.eqnt(ms):
            return True
    return False
        

def membership_temporal(m,s):
    """
    Operador de pertinença temporal. Cert quan la mesura `m` pertany
    temporalment a la sèrie temporal `s`.

    Cerca si m.t pertany al conjunt de temps de s (s.t())
    Sempre es compleix que si membership(m,S)==True aleshores
    membership_temporal(m,S)==True

    :param m: 
    :type m: :class:`Measure`
    :param s: 
    :type s: :class:`TimeSeries`
    :returns: `m ∈ᵗ s`, m pertany temporalment a s
    :rtype: bool

    >>> s = TimeSeriesSetOp([Measure(1,2)])
    >>> m1 = Measure(1,2)
    >>> m2 = Measure(1,1)
    >>> membership_temporal(m1,s)
    True
    >>> membership_temporal(m2,s)
    True
    >>> membership_temporal(Measure(2,2),s)
    False
    """
    return m.t in s.t()


def subset(s1,s2):
    """
    Operador de subconjunt. Cert quan la sèrie temporal `s1` està
    inclosa a la sèrie temporal `s2`.

    :param s1: 
    :type s1: :class:`TimeSeries`
    :param s2: 
    :type s2: :class:`TimeSeries`
    :returns: `s1 ⊆ s2`, s1 inclosa a s2
    :rtype: bool

    >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,1)])
    >>> s3 = TimeSeriesSetOp([Measure(1,5)])
    >>> subset(s1,s2)
    True
    >>> subset(s2,s1)
    False
    >>> subset(s3,s1)
    False
    >>> subset(s1,s3)
    False
    """
    for m1 in s1:
        if not membership(m1,s2):
            return False
    return True

def subset_temporal(s1,s2):
    """
    Operador de subconjunt temporal. Cert quan la sèrie temporal `s1` està
    inclosa temporalment a la sèrie temporal `s2`.
    
    Sempre es compleix que si subset(s1,s2)==True aleshores
    subset_temporal(s1,s2)==True

    :param s1: 
    :type s1: :class:`TimeSeries`
    :param s2: 
    :type s2: :class:`TimeSeries`
    :returns: `s1 ⊆ᵗ s2`, s1 inclosa temporalment a s2
    :rtype: bool

    >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,1)])
    >>> s3 = TimeSeriesSetOp([Measure(1,5)])
    >>> subset_temporal(s1,s2)
    True
    >>> subset_temporal(s2,s1)
    False
    >>> subset_temporal(s1,s3)
    False
    >>> subset_temporal(s3,s1)
    True
    """
    for m1 in s1:
        if not membership_temporal(m1,s2):
            return False
    return True






def _tb(s1,s2):
    pass

    

def union(s1,s2):
    """
    Operador d'unió. Sèrie temporal resultant d'unir les sèries
    temporals `s1` i `s2`.

    :param s1: 
    :type s1: :class:`TimeSeries`
    :param s2: 
    :type s2: :class:`TimeSeries`
    :returns: `s1 ∪ s2`, s1 unió s2
    :rtype: :class:`TimeSeries`

    >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> union(s2,s1) == s2
    True
    >>> union(s1,s2) == TimeSeries([Measure(1,2), Measure(3,2), Measure(2,1)])
    True
    """
    s = s1.copy()
    for m2 in s2:
        if not membership_temporal(m2,s):
            s.add(m2)
    return s


def union_temporal(s1,s2):
    """
    Operador d'unió temporal. Sèrie temporal resultant d'unir
    temporalment les sèries temporals `s1` i `s2`.

    :param s1: 
    :type s1: :class:`TimeSeries`
    :param s2: 
    :type s2: :class:`TimeSeries`
    :returns: `s1 ∪ᵗ s2`, s1 unió temporal s2
    :rtype: :class:`TimeSeries`

    >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> union(s2,s1) == s2
    True
    >>> union(s1,s2) == TimeSeries([Measure(1,2), Measure(3,2), Measure(2,1)])
    True
    """
    from timeseries import TimeSeries
    s = type(s1)()
    for m1 in s1:
        if not membership_temporal(m1,s2):
            s.add(m1)
        elif membership(m1,s2):
            s.add(m1)

    for m2 in s2:
        if not membership_temporal(m2,s1):
            s.add(m2)
    return s



