# -*- encoding: utf-8 -*-

"""
=============================================
Operadors de seqüència per a sèries temporals
=============================================

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació dels operadors de seqüència de Sèrie Temporal.
"""

from operator import lt, le

from measure import Measure
from structure import TimeSeriesStructure

from opset import selection, union, difference



def interval(self,l=None,g=None,openl=True,openg=True):
    """
    Operador d'interval. Sèrie temporal resultant de l'interval sobre
    la seqüència entre dos temps `l` i `g` i amb continuïtat segons
    `left`i `right`.

    :param l: Instant de temps menor
    :type l: :data:`timeseries.Time`
    :param g:  Instant de temps major
    :type g: :data:`timeseries.Time`
    :returns: `s(l,g)`
    :rtype: :class:`timeseries.TimeSeries`

    >>> s = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> interval(s,1,3,openl=True,openg=True) == TimeSeriesStructure([Measure(2,2)])
    True
    >>> interval(s,1,3,False,False) == s
    True
    """
    if openl:
        fleft = lt     
    else:
        fleft = le

    if openg:
        fright = lt     
    else:
        fright = le


    #Si els límits no existeixen seran inf(s) i sup(s) o bé -infinit i +infinit?
    if l is None:
        l = -float("inf")#no pot ser inf que no és genèric
    if g is None:
        g = float("inf")#no pot ser inf que no és genèric

    
    return selection(self,lambda m: fleft(l,m.t) and fright(m.t,g))



def interval_open(self,l,g):
    """
    Operador d'interval obert. Sèrie temporal resultant de
    l'interval sobre la seqüència entre dos temps `l` i `g`.

    :param l: Instant de temps menor
    :type l: :data:`timeseries.Time`
    :param g:  Instant de temps major
    :type g: :data:`timeseries.Time`
    :returns: `s(l,g)`
    :rtype: :class:`timeseries.TimeSeries`

    >>> s = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> interval_open(s,1,3) == TimeSeriesStructure([Measure(2,2)])
    True
    >>> interval_open(s,0,4) == s
    True
    >>> interval_open(s,float("-inf"),float("inf")) == s
    True
    >>> interval_open(s,1,1) == TimeSeriesStructure([])
    True
    """
    return interval(self,l,g,openl=True,openg=True)


def interval_closed(self,l,g):
    """
    Operador d'interval tancat. Sèrie temporal resultant de l'interval sobre la seqüència entre dos temps `l` i `g`.

    :param l: Instant de temps menor
    :type l: :data:`timeseries.Time`
    :param g:  Instant de temps major
    :type g: :data:`timeseries.Time`
    :returns: `s[l,g]`
    :rtype: :class:`timeseries.TimeSeries`

    >>> s = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> interval_closed(s,1,3) == s
    True
    >>> interval_closed(s,float("-inf"),float("inf")) == s
    True
    >>> interval_closed(s,2,2) == TimeSeriesStructure([Measure(2,2)])
    True
    """
    return interval(self,l,g,openl=False,openg=False)



def interval_open_left(self,l,g):
    """
    Operador d'interval semiobert esquerre. Sèrie temporal resultant de l'interval sobre la seqüència entre dos temps `l` i `g`.

    :param l: Instant de temps menor
    :type l: :data:`timeseries.Time`
    :param g:  Instant de temps major
    :type g: :data:`timeseries.Time`
    :returns: `s(l,g]`
    :rtype: :class:`timeseries.TimeSeries`

    >>> s = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> interval_open_left(s,1,3) == TimeSeriesStructure([Measure(2,2),Measure(3,2)])
    True
    >>> interval_open_left(s,0,4) == s
    True
    >>> interval_open_left(s,float("-inf"),float("inf")) == s
    True
    >>> interval_open_left(s,1,1) == TimeSeriesStructure([])
    True
    """
    return interval(self,l,g,openl=True,openg=False)


def interval_open_right(self,l,g):
    """
    Operador d'interval semiobert dret. Sèrie temporal resultant de l'interval sobre la seqüència entre dos temps `l` i `g`.

    :param l: Instant de temps menor
    :type l: :data:`timeseries.Time`
    :param g:  Instant de temps major
    :type g: :data:`timeseries.Time`
    :returns: `s[l,g)`
    :rtype: :class:`timeseries.TimeSeries`

    >>> s = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> interval_open_right(s,1,3) == TimeSeriesStructure([Measure(2,2),Measure(1,2)])
    True
    >>> interval_open_right(s,0,4) == s
    True
    >>> interval_open_right(s,float("-inf"),float("inf")) == s
    True
    >>> interval_open_right(s,1,1) == TimeSeriesStructure([])
    True
    """        
    return interval(self,l,g,openl=False,openg=True)




def next(self,m):
    """ 
    Mesura següent. Successor de m en s.

    :param m:
    :type m: :class:`measure.Measure`
    :return: `nextₛ(m)`, successor de m
    :rtype: :class:`measure.Measure`

    >>> m1 = Measure(1,2); m2 = Measure(2,2); m3 = Measure(3,2)
    >>> s = TimeSeriesStructure([m1,m2,m3])
    >>> next(s,m2) == m3
    True
    >>> next(s,max(s)).isundefinedp()
    True
    >>> mi = Measure(un='-')
    >>> next(s,mi) == m1
    True
    >>> s2 = TimeSeriesStructure([])
    >>> next(s2,m2).isundefinedp()
    True
    >>> next(s2,mi).isundefinedp()
    True
    >>> s.add(mi)
    >>> next(s,mi) == m1
    True
    """
    return interval_open_left(self,m.t,None).inf()

def prev(self,m):
    """ 
    Mesura anterior. Predecessor de m en s.

    :param m:
    :type m: :class:`measure.Measure`
    :return: `prevₛ(m)`, predeccessor de m
    :rtype: :class:`measure.Measure`

    >>> m1 = Measure(1,2); m2 = Measure(2,2); m3 = Measure(3,2)
    >>> s = TimeSeriesStructure([m1,m2,m3])
    >>> prev(s,m2) == m1
    True
    >>> prev(s,min(s)).isundefinedn()
    True
    >>> mi = Measure(un='+')
    >>> prev(s,mi) == m3
    True
    >>> s2 = TimeSeriesStructure([])
    >>> prev(s2,m2).isundefinedn()
    True
    >>> prev(s2,mi).isundefinedn()
    True
    >>> s.add(mi)
    >>> prev(s,mi) == m3
    True
    """
    return interval_open_right(self,None,m.t).sup()


def concatenate(self,s):
    """ 
    Concatenació amb una altra sèrie temporal.

    :param s:
    :type s: :class:`timeseries.TimeSeries`
    :return: `s1 || s2`, concatenació amb s
    :rtype: :class:`timeseries.TimeSeries`

    >>> s = TimeSeriesStructure([])
    >>> s1 = TimeSeriesStructure([Measure(4,1),Measure(1,1),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(5,2),Measure(0,2)])
    >>> concatenate(s1,s2) == TimeSeriesStructure([Measure(4,1),Measure(1,1),Measure(2,1),Measure(5,2),Measure(0,2)])
    True
    >>> concatenate(s2,s1) == s2
    True
    >>> concatenate(s,s1) == s1
    True
    >>> concatenate(s1,s) == s1
    True
    >>> concatenate(s1,s1) == s1
    True
    """
    t1 = self.inf().t
    t2 = self.sup().t
    return union(self, difference(s, interval_closed(s,t1,t2)))






