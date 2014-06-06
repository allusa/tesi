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
  

#'isdisjoint', 'issubset', 'issuperset', __contains__




"""
No Temporal
===========
"""

def membership(s,m):
    """
    Operador de pertinença. Cert quan la mesura `m` pertany a la sèrie
    temporal `s`.

    :param s: 
    :param m: 
    :type s: :class:`TimeSeries`
    :type m: :class:`Measure`
    :returns: `m ∈ s`, m pertany a s
    :rtype: bool

    >>> s = TimeSeriesSetOp([Measure(1,2)])
    >>> m1 = Measure(1,2)
    >>> m2 = Measure(1,1)
    >>> membership(s,m1)
    True
    >>> membership(s,m2)
    False
    """
    for ms in s:
        if m.eqp(ms):
            return True
    return False


def union(s1, s2):
    """
    Operador d'unió. Sèrie temporal resultant d'unir la sèrie
    temporal `s1` amb `s2`.

    :param s1: 
    :param s2: 
    :type s1: :class:`TimeSeries`
    :type s2: :class:`TimeSeries`
    :returns: `s1 ∪ s2`, s1 unió s2
    :rtype: :class:`TimeSeries`

    >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> union(s2,s1) == s2
    True
    >>> union(s1,s2) == TimeSeriesSetOp([Measure(1,2), Measure(3,2), Measure(2,1)])
    True
    """
    s = s1.copy()
    for m2 in s2:
        if not membership_temporal(s,m2):
            s.add(m2)
    return s



def difference(s1, s2):
    """
    Operador de diferència Sèrie temporal resultant de treure
    `s2` de la sèrie temporal `s1`.

    :param s1: 
    :param s2: 
    :type s1: :class:`TimeSeries`
    :type s2: :class:`TimeSeries`
    :returns: `s1 - s2`, s1 diferència s2
    :rtype: :class:`TimeSeries`

    >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> difference(s1,s1) == TimeSeriesSetOp([])
    True
    >>> difference(s1,s2) == TimeSeriesSetOp([Measure(2,1)])
    True
    >>> difference(s2,s1) == TimeSeriesSetOp([Measure(2,2),Measure(3,2)])
    True
    """
    s = s1.empty()
    for m1 in s1:
        if not membership(s2,m1):
            s.add(m1)
    return s


def intersection(s1, s2):
    """
    Operador d'intersecció. Sèrie temporal resultant
    d'interseccionar `s1` amb la sèrie temporal `s2`.

    :param s1: 
    :param s2: 
    :type s1: :class:`TimeSeries`
    :type s2: :class:`TimeSeries`
    :returns: `s1 ∩ s2`, s1 intersecció s2
    :rtype: :class:`TimeSeries`

    >>> s1 = TimeSeriesSetOp([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesSetOp([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> intersection(s1,s1) == s1
    True
    >>> intersection(s1,s2) == TimeSeriesSetOp([Measure(1,2)])
    True
    >>> intersection(s2,s1) == intersection(s1,s2)
    True
    """
    return difference(s1,difference(s1,s2))





"""
Temporal
========
"""




def membership_temporal(s,m):
    """
    Operador de pertinença temporal. Cert quan la mesura `m` pertany
    temporalment a la sèrie temporal `s`.

    Cerca si m.t pertany al conjunt de temps de s (s.t())
    Sempre es compleix que si membership(s,m)==True aleshores
    membership_temporal(s,m)==True

    :param s:
    :param m: 
    :type s: :class:`TimeSeries`
    :type m: :class:`Measure`
    :returns: `m ∈ᵗ s`, m pertany temporalment a s
    :rtype: bool

    >>> s = TimeSeriesSetOp([Measure(1,2)])
    >>> m1 = Measure(1,2)
    >>> m2 = Measure(1,1)
    >>> membership_temporal(s,m1)
    True
    >>> membership_temporal(s,m2)
    True
    >>> membership_temporal(s,Measure(2,2))
    False
    """
    return m.t in s.t()






"""
Mixins
======
"""



class SetOpNoTemporalMixin():
    """
    Operadors de conjunts no temporals de Sèrie Temporal
    """   
    from opset import membership, union, difference


class SetOpTemporalMixin():
    """
    Operadors de conjunts temporals de Sèrie Temporal
    """   
    from opset import membership_temporal



#sobre Mixins 
#Part1 http://www.artima.com/weblogs/viewpost.jsp?thread=246341 
#Part2 http://www.artima.com/weblogs/viewpost.jsp?thread=246483


#proves
class TimeSeriesMixed(SetOpTemporalMixin,SetOpNoTemporalMixin,TimeSeriesStructure):
    """
    >>> s1 = TimeSeriesMixed([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesMixed([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> s2.union(s1) == s2
    True
    """
    pass






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
            if m.eqp(ms):
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
        `other` de la sèrie temporal.

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
        s = self.empty()
        for m1 in self:
            if not other.membership(m1):
                s.add(m1)
        return s

    def intersection(self, other):
        """
        Operador d'intersecció. Sèrie temporal resultant
        d'interseccionar `other` amb la sèrie temporal.

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
        de la diferènca simètrica d'`other` amb la sèrie temporal.

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
        s = self.empty()
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
        treure temporalment `other` de la sèrie temporal.

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
        s = self.empty()
        for m1 in self:
            if not other.membership_temporal(m1):
                s.add(m1)
        return s

    def intersection_temporal(self, other):
        """
        Operador d'intersecció temporal. Sèrie temporal resultant
        d'interseccionar temporalment `other` amb la sèrie temporal.

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
        de la diferènca simètrica temporal d'`other` amb la sèrie temporal.

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
        Operador de projecció. Conjunt resultant de seleccionar els
        atributs (columnes) `A` de la sèrie temporal.  

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
        >>> s2 = TimeSeriesSetOp([Measure(1,[1,2]),Measure(2,[1,2])])
        >>> s2.projection(['t','v0'])  == set([(1,1),(2,1)])
        True
        >>> s2.projection(['t','v1'])  == set([(1,2),(2,2)])
        True
        >>> s2.projection(['t','v0','v1']) == set([(1,1,2),(2,1,2)])
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
                elif a.startswith('v'):
                    i = int(a[1:])
                    row.append(m.v[i])

            if len(row) > 1:
                s.add(tuple(row))
            elif len(row) == 1:
                s.add(row[0])
            else:
                pass
        return s

    def selection(self,f):
        """
        Operador de selecció. Sèrie temporal resultant de seleccionar els
        tuples (files) de la sèrie temporal segon la funció booleana
        `f`.

        :param f: funció booleana de selecció, f(m)->bool
        :type f: function of Measure returns bool
        :returns: `s where f`, selecció de s en f
        :rtype: :class:`TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,1),Measure(2,1),Measure(4,1)])
        >>> def t_gt_1(m):
        ...     return m.t > 1
        >>> TimeSeriesSetOp([]).selection(t_gt_1) == set()
        True
        >>> s1.selection(t_gt_1) == TimeSeriesSetOp([Measure(2,1),Measure(4,1)])
        True
        >>> s1.selection(lambda m: m.t > 1) == TimeSeriesSetOp([Measure(2,1),Measure(4,1)])
        True
        """
        l = filter(f,self)
        s = self.empty()
        s.update(l)
        return s


    def product(self,other):
        """
        Operador de producte. Conjunt resultant de fer el producte
        cartesià amb una altra sèrie temporal.

        :param other:
        :type other: :class:`TimeSeries`
        :returns: `s1 x s2`, producte de s1 per s2
        :rtype: set

        >>> s1 = TimeSeriesSetOp([Measure(1,1),Measure(2,1)])
        >>> s2 = TimeSeriesSetOp([Measure(1,2),Measure(3,2)])
        >>> s1.product(s2) == set([(1,1,1,2),(1,1,3,2),(2,1,1,2),(2,1,3,2)])
        True
        >>> s2.product(s1) == set([(1,2,1,1),(3,2,1,1),(1,2,2,1),(3,2,2,1)])
        True
        """
        s = set()
        for m1 in self:
            for m2 in other:
                s.add( (m1.t,m1.v,m2.t,m2.v) )
        return s
 
    def join(self,other):
        """
        Operador de junció. Sèrie temporal resultant d'ajuntar amb una
        altra sèrie temporal.

        :param other:
        :type other: :class:`TimeSeries`
        :returns: `s1 join s2`, junció de s1 amb s2
        :rtype: :class:`TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,1),Measure(2,1)])
        >>> s2 = TimeSeriesSetOp([Measure(1,2),Measure(3,2)])
        >>> s1.join(s2) == TimeSeriesSetOp([Measure(1,(1,2))])
        True
        >>> s2.join(s1) == TimeSeriesSetOp([Measure(1,(2,1))])
        True
        """
        s = self.empty()
        p = self.product(other)
        for (t1,v1,t2,v2) in p:
            if t1==t2:
                s.add(Measure(t1,(v1,v2)))
        return s


    def map(self,f):
        """
        Operador de mapa. Sèrie temporal resultant de mapar amb la
        funció `f`.

        :param f: funció de mapatge, f(m)->m
        :type f: function of Measure returns Measure
        :returns: `map(s,f)`, mapa de f a s
        :rtype: :class:`TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,1),Measure(2,1)])
        >>> s1.map(lambda m: Measure(m.t,m.v*2)) == TimeSeriesSetOp([Measure(1,2),Measure(2,2)])
        True
        """
        s = self.empty()
        s.update(map(f,self))
        return s

    def aggregate(self,f,mi=None):
        """
        Operador d'agregació. Sèrie temporal resultant d'agregar amb
        la funció `f` a partir de la mesura inicial `mi` (opcional en
        alguns casos).

        :param mi: mesura inicial, optional in some cases
        :type mi: :class:`measure.Measure`
        :param f: funció d'agregació, f(m1,m2)->m
        :type f: function of two Measures returns Measure
        :returns: `aggregate(s,mi,f)`, agregat de s segons f iniciat a mi
        :rtype: :class:`measure.Measure`

        >>> s1 = TimeSeriesSetOp([Measure(1,1),Measure(2,1)])
        >>> s1.aggregate(lambda mi,m: Measure(0,mi.v+m.v), Measure(0,0)) == Measure(0,2)
        True
        >>> s1.aggregate(lambda mi,m: Measure(0,mi.v+m.v)) == Measure(0,2)
        True
        """
        if mi is None:
            return reduce(f,self)
        return reduce(f,self,mi)

    def fold(self,f,si=None):
        """
        Operador de plec. Sèrie temporal resultant de plegar amb
        la funció `f` a partir de la sèrie temporal inicial `si` (per defecte la sèrie temporal buida).

        :param si: sèrie temporal inicial, optional if empty si
        :type si: :class:`timeseries.TimeSeries`
        :param f: funció de plegament, f(s1,m)->s
        :type f: function of TimeSeries x Measure returns TimeSeries
        :returns: `fold(s,si,f)`, plec de s segons f iniciat a si
        :rtype: :class:`timeseries.TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,1),Measure(2,1)])
        >>> s1.fold(lambda s,m: s.union(TimeSeriesSetOp([m]))) == s1
        True
        >>> from timeseries import TimeSeries
        >>> def tpredecessors(s):
        ...     si = s.map(lambda m: Measure(m.t,float("-inf")))
        ...     def f(si,m):
        ...         t = m.t
        ...         tp = si.selection(lambda m: m.t < t).sup().t
        ...         a = TimeSeries([Measure(t,tp)])
        ...         return a.union(si)
        ...     return s.fold(f,si)
        >>> tpredecessors(s1) == TimeSeriesSetOp([Measure(1,float("-inf")),Measure(2,1)])
        True
        """
        if si is None:
            si = self.empty()
        return reduce(f,self,si)      


    def orderfold(self,f,o,si=None):
        """
        Operador de plec amb ordre. Sèrie temporal resultant de plegar
        amb la funció `f` i ordre `o` a partir de la sèrie temporal
        inicial `si` (per defecte la sèrie temporal buida).

        :param si: sèrie temporal inicial, optional if empty si
        :type si: :class:`timeseries.TimeSeries`
        :param f: funció de plegament, f(s1,m)->s
        :type f: function of TimeSeries x Measure returns TimeSeries
        :param o: funció d'ordre, o(s)->m
        :type o: function of TimeSeries returns Measure
        :returns: `fold(s,si,f,o)`, plec de s segons f i ordre o iniciat a si
        :rtype: :class:`timeseries.TimeSeries`

        >>> s1 = TimeSeriesSetOp([Measure(1,1),Measure(2,1)])
        >>> s1.orderfold(lambda s,m: s.union(TimeSeriesSetOp([m])),max) == s1
        True
        >>> s1.orderfold(lambda s,m: s.union(TimeSeriesSetOp([m])),min) == s1
        True
        >>> s1.orderfold(lambda s,m: TimeSeriesSetOp([m]),min) == TimeSeriesSetOp([Measure(2,1)])
        True
        """
        if si is None:
            si = self.empty()

        if len(self) == 0:
            return si

        m0 = o(self)
        s0 = type(self)([m0])
        so = self - s0
        return so.orderfold(f,o,f(si,m0))        



    def op(self,other,f):
        """
        Operador computacional binari entre mesures comunes. Sèrie
        temporal resultant d'aplicar l'operador `f` a la junció de la
        sèrie temporal amb `other`.

        :param other: 
        :type other: :class:`timeseries.TimeSeries`
        :param f: funció binària de mesures
        :type f: function of two Measures returns Measure
        :returns: `s1 op s2`, càlcul d'op als valors de les sèries temporals
        :rtype: :class:`timeseries.TimeSeries`        

        >>> s1 = TimeSeriesSetOp([Measure(1,1),Measure(2,1),Measure(3,1)])
        >>> s2 = TimeSeriesSetOp([Measure(1,2),Measure(3,2),Measure(5,2)])
        >>> s1.op(s2,lambda x,y: x+y) == TimeSeriesSetOp([Measure(1,3),Measure(3,3)])
        True
        """
        return self.join(other).map(lambda m: Measure(m.t,f(m.v[0],m.v[1])))


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
    >>> s1 - s2 == s1.difference(s2)
    True
    >>> s1 & s2 == s1.intersection(s2)
    True
    >>> s1 ^ s2 == s1.symmetric_difference(s2)
    True
    >>> s1 * s2 == s1.product(s2)
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











