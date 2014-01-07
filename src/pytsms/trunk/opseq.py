# -*- encoding: utf-8 -*-

"""
=============================================
Operadors de seqüència per a sèries temporals
=============================================

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació dels operadors de seqüència de Sèrie Temporal.
"""


from measure import Measure, MeasureUndefinedP, MeasureUndefinedN
from structure import TimeSeriesStructure



class TimeSeriesSeqOp(TimeSeriesStructure):
    """
    Operadors de seqüència de Sèrie Temporal

        * s[l:g] open
        * s[l:g:0] o s[l:g:'o'] open
        * s[l:g:1] o s[l:g:'c'] closed
        * s[l:g:2] o s[l:g:'l'] semiopen left
        * s[l:g:3] o s[l:g:'r'] semiopen right
        * s1 + s2

    >>> from timeseries import TimeSeries
    >>> s = TimeSeries([Measure(3,1),Measure(1,1),Measure(2,1)])
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
    >>> s2 = TimeSeries([Measure(4,2),Measure(1,2),Measure(0,2)])
    >>> s + s2 == s.concatenate(s2)
    True
    >>> s2 + s == s2.concatenate(s)
    True
    """
 
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
                          2: ['semiopen-left','l'],
                          3: ['semiopen-right','r']
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



    # 
    # public API
    #



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

        >>> s = TimeSeriesSeqOp([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s.interval_open(1,3) == TimeSeriesSeqOp([Measure(2,2)])
        True
        >>> s.interval_open(0,4) == s
        True
        >>> s.interval_open(float("-inf"),float("inf")) == s
        True
        >>> s.interval_open(1,1) == TimeSeriesSeqOp([])
        True
        """
        r = self.empty()
        for m in self:
            if m.t > l and m.t < g:
                r.add(m)
        return r

    def interval_closed(self,l,g):
        """
        Operador d'interval tancat. Sèrie temporal resultant de l'interval sobre la seqüència entre dos temps `l` i `g`.

        :param l: Instant de temps menor
        :type l: :data:`timeseries.Time`
        :param g:  Instant de temps major
        :type g: :data:`timeseries.Time`
        :returns: `s[l,g]`
        :rtype: :class:`timeseries.TimeSeries`

        >>> s = TimeSeriesSeqOp([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s.interval_closed(1,3) == s
        True
        >>> s.interval_closed(float("-inf"),float("inf")) == s
        True
        >>> s.interval_closed(2,2) == TimeSeriesSeqOp([Measure(2,2)])
        True
        """
        r = self.empty()
        for m in self:
            if m.t >= l and m.t <= g:
                r.add(m)
        return r 

    def interval_open_left(self,l,g):
        """
        Operador d'interval semiobert esquerre. Sèrie temporal resultant de l'interval sobre la seqüència entre dos temps `l` i `g`.

        :param l: Instant de temps menor
        :type l: :data:`timeseries.Time`
        :param g:  Instant de temps major
        :type g: :data:`timeseries.Time`
        :returns: `s(l,g]`
        :rtype: :class:`timeseries.TimeSeries`

        >>> s = TimeSeriesSeqOp([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s.interval_open_left(1,3) == TimeSeriesSeqOp([Measure(2,2),Measure(3,2)])
        True
        >>> s.interval_open_left(0,4) == s
        True
        >>> s.interval_open_left(float("-inf"),float("inf")) == s
        True
        >>> s.interval_open_left(1,1) == TimeSeriesSeqOp([])
        True
        """
        r = self.empty()
        for m in self:
            if m.t > l and m.t <= g:
                r.add(m)
        return r

    def interval_open_right(self,l,g):
        """
        Operador d'interval semiobert dret. Sèrie temporal resultant de l'interval sobre la seqüència entre dos temps `l` i `g`.

        :param l: Instant de temps menor
        :type l: :data:`timeseries.Time`
        :param g:  Instant de temps major
        :type g: :data:`timeseries.Time`
        :returns: `s[l,g)`
        :rtype: :class:`timeseries.TimeSeries`

        >>> s = TimeSeriesSeqOp([Measure(3,2),Measure(1,2),Measure(2,2)])
        >>> s.interval_open_right(1,3) == TimeSeriesSeqOp([Measure(2,2),Measure(1,2)])
        True
        >>> s.interval_open_right(0,4) == s
        True
        >>> s.interval_open_right(float("-inf"),float("inf")) == s
        True
        >>> s.interval_open_right(1,1) == TimeSeriesSeqOp([])
        True
        """
        r = self.empty()
        for m in self:
            if m.t >= l and m.t < g:
                r.add(m)
        return r


    def next(self,m):
        """ 
        Mesura següent. Successor de m en s.

        :param m:
        :type m: :class:`measure.Measure`
        :return: `nextₛ(m)`, successor de m
        :rtype: :class:`measure.Measure`
        
        >>> m1 = Measure(1,2); m2 = Measure(2,2); m3 = Measure(3,2)
        >>> s = TimeSeriesSeqOp([m1,m2,m3])
        >>> s.next(m2) == m3
        True
        >>> s.next(max(s)).isundefinedp()
        True
        >>> mi = MeasureUndefinedN()
        >>> s.next(mi) == m1
        True
        >>> s2 = TimeSeriesSeqOp([])
        >>> s2.next(m2).isundefinedp()
        True
        >>> s2.next(mi).isundefinedp()
        True
        >>> s.add(mi)
        >>> s.next(mi) == m1
        True
        """
        return self[m.t::'l'].inf()

    def prev(self,m):
        """ 
        Mesura anterior. Predecessor de m en s.

        :param m:
        :type m: :class:`measure.Measure`
        :return: `prevₛ(m)`, predeccessor de m
        :rtype: :class:`measure.Measure`
          
        >>> m1 = Measure(1,2); m2 = Measure(2,2); m3 = Measure(3,2)
        >>> s = TimeSeriesSeqOp([m1,m2,m3])
        >>> s.prev(m2) == m1
        True
        >>> s.prev(min(s)).isundefinedn()
        True
        >>> mi = MeasureUndefinedP()
        >>> s.prev(mi) == m3
        True
        >>> s2 = TimeSeriesSeqOp([])
        >>> s2.prev(m2).isundefinedn()
        True
        >>> s2.prev(mi).isundefinedn()
        True
        >>> s.add(mi)
        >>> s.prev(mi) == m3
        True
        """
        return self[:m.t:'r'].sup()





    def concatenate(self,s):
        """ 
        Concatenació amb una altra sèrie temporal.

        :param s:
        :type s: :class:`timeseries.TimeSeries`
        :return: `s1 || s2`, concatenació amb s
        :rtype: :class:`timeseries.TimeSeries`

        >>> s = TimeSeriesSeqOp([])
        >>> s1 = TimeSeriesSeqOp([Measure(4,1),Measure(1,1),Measure(2,1)])
        >>> s2 = TimeSeriesSeqOp([Measure(3,2),Measure(1,2),Measure(5,2),Measure(0,2)])
        >>> s1.concatenate(s2) == TimeSeriesSeqOp([Measure(4,1),Measure(1,1),Measure(2,1),Measure(5,2),Measure(0,2)])
        True
        >>> s2.concatenate(s1) == s2
        True
        >>> s.concatenate(s1) == s1
        True
        >>> s1.concatenate(s) == s1
        True
        >>> s1.concatenate(s1) == s1
        True
        """
        t1 = self.inf().t
        t2 = self.sup().t
        return self.union(s-s[t1:t2:'c'])


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
            
