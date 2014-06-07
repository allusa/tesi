# -*- encoding: utf-8 -*-

"""
=========================================
Mixins d'operadors per a sèries temporals
=========================================

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació dels mixins per als opereadors de Sèrie Temporal.
"""


from measure import Measure
from structure import TimeSeriesStructure




#sobre Mixins 
#Part1 http://www.artima.com/weblogs/viewpost.jsp?thread=246341 
#Part2 http://www.artima.com/weblogs/viewpost.jsp?thread=246483



"""
Set
===
"""



class SetOpNoTemporalMixin():
    """
    Operadors de conjunts no temporals de Sèrie Temporal
    """   
    from opset import membership, subset, union, difference, symmetric_difference

class SetOpTemporalMixin():
    """
    Operadors de conjunts temporals de Sèrie Temporal
    """   
    from opset import membership_temporal, subset_temporal, union_temporal, difference_temporal, symmetric_difference_temporal


class SetOpRelationalMixin():
    """
    Operadors de conjunts relacionals de Sèrie Temporal
    """   
    from opset import selection, projection, product, join, fold, aggregate, orderfold, op
    from opset import mapp as map



class SetOpMixin(SetOpRelationalMixin, SetOpTemporalMixin, SetOpNoTemporalMixin):
    """
    Operadors de conjunts de Sèrie Temporal
    """   
    def __or__(self, other):
        """
        Binary arithmetic operation union for sets, symbol `|`.
        """
        return self.union(other)

    def __sub__(self, other):
        """
        Binary arithmetic operation difference for sets, symbol `-`.
        """
        return self.difference(other)

    def __and__(self, other):
        """
        Binary arithmetic operation intersection for sets, symbol `&`.
        """
        return self.intersection(other)

    def __xor__(self, other):
        """
        Binary arithmetic operation symmetric difference for sets, symbol `^`.
        """
        return self.symmetric_difference(other)


    def __mul__(self, other):
        """
        Binary arithmetic operation product, symbol `*`.
        """
        return self.product(other)



    
    def filter(self, f):
        """
        Functional programming tool filter is :meth:`TimeSeriesSetOpRelacional.selection`.
        """
        return self.selection(f)

    def reduce(self, f, mi=None):
        """
        Functional programming tool reduce is :meth:`TimeSeriesSetOpRelacional.aggregate`.
        """
        return self.aggregate(f,mi)




#proves
class TimeSeriesMixed(SetOpMixin,TimeSeriesStructure):
    """
    >>> s1 = TimeSeriesMixed([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesMixed([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> s2.union(s1) == s2
    True
    """
    pass
