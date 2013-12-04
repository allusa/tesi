# -*- encoding: utf-8 -*-

"""
================
Sèries temporals
================

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació de Sèrie Temporal.
"""


from measure import Measure
from structure import TimeSeriesStructure
from opset import TimeSeriesSetOp, TimeSeriesSetOpTemporal




class TimeSeries(TimeSeriesSetOp,TimeSeriesStructure):
    """
    L'ordre de l'herència és important, `TimeSeriesStructure` ha d'anar
    en darrer lloc per tal que les seves operacions siguin
    redefinides.


    Binary arithmetic operations:
    
    * union for sets, symbol `|` (or), method `union`


    >>> s1 = TimeSeries([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeries([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> s2 | s1 == s2
    True
    >>> s1 | s2 == TimeSeries([Measure(1,2), Measure(3,2), Measure(2,1)])
    True
    >>> s1 | s2 == s1.union(s2)
    True
    >>> s1.temporal() | s2 == TimeSeries([Measure(1,2), Measure(3,2)])
    True
    >>> s1.temporal() | s2 == s1.union_temporal(s2)
    True
    """


    def temporal(self):
        """
        Per a cridar els operadors de conjunts temporals
        """
        s = self.copy()
        s.__class__ = TimeSeriesTemporal
        return s



class TimeSeriesTemporal(TimeSeriesSetOpTemporal,TimeSeries):


    def _notemporal(self):
        """
        Per a no cridar els operadors de conjunts temporals
        """
        s = self.copy()
        s.__class__ = TimeSeries
        return s





def _s1test():
    """
    Retorna una sèrie temporal de prova
    """
    m1 = Measure(1,10)
    m2 = Measure(2,10)
    m3 = Measure(5,40)

    s = SerieTemporal() 
    s.add(m1)
    s.add(m2)
    s.add(m3)

    return s






# class TimeSeriesTemporal(TimeSeries):
#     """
#     Sèrie Temporal per a operacions temporals

#     >>> import opset
#     >>> s1 = TimeSeriesTemporal([Measure(1,2),Measure(2,1)])
#     >>> s2 = TimeSeriesTemporal([Measure(3,2),Measure(1,2),Measure(2,2)])
#     >>> print s1 | s2
#     >>> s1 | s2 == opset.union_temporal(s1,s2)
#     True
#     >>> s2 | s1 == opset.union_temporal(s2,s1)
#     True
#     """


#     def __in__(self,m):
#         """
#         Pertinença temporal exclusiva, només certa si m pertany
#         temporalment a s i no pertany a s. Equivalent a ta.
#         """
#         if TimeSeries.__in__(self,m):
#             for ms in self:
#                 if ms.eqnt(m):
#                     return False
#             return True
#         return False













class SerieTemporal(set):
    def __init__(self):
        raise DeprecationWarning("Useu TimeSeries")

    def __getitem__(self,key):
        """
        Definició d'element i interval d'elements en una sèrie temporal. Definició contínua per l'esquerra:

        `s[r:t]` correspon a la definició S(r,t] on r i t són dos temps. `s[r:]`correspon a la definició S(r,infinit), així com `s[:t]`correspon a S(-infinit,t] i `s[:]`correspon a S(-infinit,infinit).

        `s["-i":t]` correspon a S[-infinit,t).


        Per implementació a Python cal definir l'element `s[i]`, el qual es fa correspondre amb m in S: T(m) = i

        :param key: Element S(i) o interval d'elements S(r:t) 
        :type key: int or slice

        """
        """
        >>> s = _s1test()
        >>>
        >>> s[1:5]
        SerieTemporal([m(10,2), m(40,5)])
        >>> s[1:10]
        SerieTemporal([m(10,2), m(40,5)])
        >>> s[1:]
        SerieTemporal([m(10,2), m(40,5)])
        >>> s[5:5]
        SerieTemporal([])
        >>> s[:] == s
        True
        >>> s[-float("inf"):float("inf")] == s
        True
        >>> s[:5]
        SerieTemporal([m(10,1), m(10,2), m(40,5)])
        >>> s["-i":5]
        SerieTemporal([m(10,1), m(10,2)])
        >>> s[float("inf"):5]
        SerieTemporal([])
        >>> s[0:-float("inf")]
        SerieTemporal([])
        >>> 
        >>> s2 = SerieTemporal()
        >>> s2[:]
        SerieTemporal([])
        >>> s2[float("inf"):-float("inf")]
        SerieTemporal([])
        >>> s2["-i":5]
        SerieTemporal([])
        """

        #interval d'elements
        if isinstance(key,slice):    
            l = key.start
            g = key.stop
            p = key.step
 

            #Per definició, S(r,infinit] serà S(r,T(sup(S))]
            if g is None:
                g = float("inf")
            #Per definició, S(-infinit,t] serà S(T(inf(S)),t]
            if l is None:
                l = -float("inf")


            #Per pacte, S["-i":t] és S[-infinit,t)
            if l == '-i':
                l = self.inf().t
                s = SerieTemporal()
                for m in self:
                    if m.t >= l and m.t < g:
                        s.add(m)
                return s


            s = SerieTemporal()
            for m in self:
                if m.t > l and m.t <= g:
                    s.add(m)
            return s

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


    def sup(self):
        """
        Suprem de la sèrie temporal

        :returns: La mesura suprema de S
        :rtype: mesura

        """
        """
        >>> s = _s1test() 
        >>> s.sup()
        m(40,5)
        >>> s2 = SerieTemporal()
        >>> s2.sup()
        m(inf,-inf)
        """
        if len(self) == 0:
            return Measure(float("inf"),-float("inf"))
        else:
            return max(self)

    def inf(self):
        """
        Ínfim de la sèrie temporal

        :returns: La mesura ínfima de S
        :rtype: mesura

        """
        """
        >>> s = _s1test() 
        >>> s.inf()
        m(10,1)
        >>> s2 = SerieTemporal()
        >>> s2.inf()
        m(inf,inf)
        """
        if len(self) == 0:
            return Measure(float("inf"),+float("inf"))
        else:
            return min(self)


    def seg(self,m):
        """ 
        Measure següent. Successor de m en S.

        :type m: mesura
        :returns: La mesura següent a m
        :rtype: mesura
        
        """
        """
        >>> m1 = Measure(10,1)
        >>> m2 = Measure(10,2)
        >>> m3 = Measure(20,5)
        >>> s = SerieTemporal()
        >>> s.add(m1)
        >>> s.add(m2)
        >>> s.add(m3)
        >>>
        >>> s.seg(m2)
        m(20,5)
        >>> s.seg(max(s))
        m(inf,inf)
        >>> mi = Measure(float("inf"),-float("inf"))
        >>> s.seg(mi)
        m(10,1)
        >>>
        >>> s2 = SerieTemporal()
        >>> s2.seg(m2)
        m(inf,inf)
        >>> s2.seg(mi)
        m(inf,inf)
        >>> s.add(mi)
        >>> s.seg(mi)
        m(10,1)
        """
        s = self
        return s[m.t:].inf()

    def ant(self,m):
        """ 
        Measure anterior. Predecessor de m en S.

        :type m: mesura
        :returns: La mesura anterior a m
        :rtype: mesura
        
        """
        """
        >>> m1 = Measure(10,1)
        >>> m2 = Measure(10,2)
        >>> m3 = Measure(20,5)
        >>> s = SerieTemporal()
        >>> s.add(m1)
        >>> s.add(m2)
        >>> s.add(m3)
        >>>
        >>> s.ant(m2)
        m(10,1)
        >>> s.ant(min(s))
        m(inf,-inf)
        >>> mi = Measure(float("inf"),float("inf"))
        >>> s.ant(mi)
        m(20,5)
        >>>
        >>> s2 = SerieTemporal()
        >>> s2.ant(m2)
        m(inf,-inf)
        >>> s2.ant(mi)
        m(inf,-inf)
        >>> s.add(mi)
        >>> s.ant(mi)
        m(20,5)
        """
        s = self
        return s["-i":m.t].sup()


    def __repr__(self):
        """
        Sobrecàrrega del mètode representació per tal que sempre es
        representi ordenat.
        """
        return 'SerieTemporal({0})'.format( repr(sorted(self)) )



    def esRegular(self):
        """
        Predicat que és cert ssi la sèrie temporal és regular

        """
        """
        >>> s = _s1test()
        >>> s.esRegular()
        False
        >>> s2 = SerieTemporal()
        >>> s2.add(Measure(10,3));s2.add(Measure(10,6));s2.add(Measure(25,9));s2.add(Measure(10,12))
        >>> s2.esRegular()
        True
        """
        r = min(self)
        s = self[r.t:] #S(r,infinit)

        prevdelta = None

        for m in s:
            delta = m.t - self.ant(m).t
            if not prevdelta:
                prevdelta = delta
            elif delta == prevdelta:
                prevdelta = delta
            else:
                return False

        return True


