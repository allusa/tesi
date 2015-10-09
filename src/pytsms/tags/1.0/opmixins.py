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



class SetOpMixin(
    SetOpRelationalMixin, 
    SetOpTemporalMixin, 
    SetOpNoTemporalMixin):
    """
    Operadors de conjunts de Sèrie Temporal

    >>> class TimeSeriesMixed(SetOpMixin,TimeSeriesStructure): pass
    >>> s1 = TimeSeriesMixed([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesMixed([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> s2.union(s1) == s2
    True
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






class SeqOpMixin():
    """
    Operadors de seqüència de Sèrie Temporal

        * s[l:g] open
        * s[l:g:0] o s[l:g:'o'] open
        * s[l:g:1] o s[l:g:'c'] closed
        * s[l:g:2] o s[l:g:'l'] semiopen left
        * s[l:g:3] o s[l:g:'r'] semiopen right
        * s1 + s2

    >>> class TimeSeriesMixed(SeqOpMixin,TimeSeriesStructure): pass
    >>> s = TimeSeriesMixed([Measure(3,1),Measure(1,1),Measure(2,1)])
    >>> s[1:3] == s.interval_open(1,3)
    True
    >>> s[1:3:1] == s.interval_closed(1,3)
    True
    >>> s[1:3:'c'] == s.interval_closed(1,3)
    True
    >>> s[1:3:6]
    Traceback (most recent call last):
    ...
    KeyError: 'Step error'
    >>> s[1:1] == s.interval_open(1,1)
    True
    >>> s[0:] == s
    True
    >>> s[:] == s
    True
    >>> s2 = TimeSeriesMixed([Measure(4,2),Measure(1,2),Measure(0,2)])
    >>> s + s2 == s.concatenate(s2)
    True
    >>> s2 + s == s2.concatenate(s)
    True
    """
    
    from opseq import interval, interval_open, interval_closed, interval_open_right, interval_open_left, next, prev, concatenate


 
    def __getitem__(self,key):
        """
        Definició d'element i interval d'elements en seqüències. 

        * s[l:g] open
        * s[l:g:0] o s[l:g:'o'] open
        * s[l:g:1] o s[l:g:'c'] closed
        * s[l:g:2] o s[l:g:'l'] semiopen left
        * s[l:g:3] o s[l:g:'r'] semiopen right
        """

        #interval d'elements
        if isinstance(key,slice):    
            l = key.start
            g = key.stop
            p = key.step
 
            #Si els límits no existeixen seran inf(s) i sup(s) o bé -infinit i +infinit?
            if g is None:
                g = float("inf")#no pot ser inf que no és genèric
            if l is None:
                l = -float("inf")

            #step marca obert, tancat, semiobert dret i semiobert esquerre
            stepvocab = { 0: ['open','o'],
                          1: ['closed','c'],
                          2: ['semiopen-left','l','open-left','ol','closed-right','cr'],
                          3: ['semiopen-right','r','open-right','or','closed-left','cl']
                          }
            if p is None:
                p = 0
            

            if p==0 or p in stepvocab[0]:
                return self.interval_open(l,g)
            elif p==1 or p in stepvocab[1]:
                return self.interval_closed(l,g)
            elif p==2 or p in stepvocab[2]:
                return self.interval_open_left(l,g)
            elif p==3 or p in stepvocab[3]:
                return self.interval_open_right(l,g)
        
            else:
                raise KeyError('Step error')

        #element, no definit en el model però necessari per Python
        else:
            #mesura màxima i mínima de la sèrie temporal
            minm = min(self)
            maxm = max(self)

            l = key
            g = key

            if l < minm.t or g > maxm.t:
                raise IndexError()
            for m in self:
                if m.t == key:
                    return m
          
        raise KeyError



    def __add__(self,other):
        """
        Concatenació en seqüències. 

        * s1 + s2
        """
        return self.concatenate(other)


    def append(self,m):
        """ 
        Modificador. Com l'add per als conjunts però ara com a seqüència controla que m.t > self.sup().t

        :param m:
        :type m: :class:`measure.Measure`
        :return: sèrie temporal amb m afegida si és posterior a la mesura suprema
        :rtype: :class:`timeseries.TimeSeries`
        :raises IndexError: if measure `m` not subsequent in time"
        """
        if len(self) == 0 or m.t > self.sup().t:
            self.add(m)
        elif m.t <= self.sup().t :
            raise IndexError("Measure not subsequent in time")
            

