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

    >>> s = TimeSeriesStructure([Measure(1,2)])
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


def subset(s1,s2):
    """
    Operador de subconjunt. Cert quan la sèrie temporal `s1` està
    inclosa a la sèrie temporal `s2`.

    :param s1: 
    :param s2: 
    :type s1: :class:`TimeSeries`
    :type s2: :class:`TimeSeries`
    :returns: `s1 ⊆ s2`, s1 inclosa a s2
    :rtype: bool

    >>> s1 = TimeSeriesStructure([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,1)])
    >>> s3 = TimeSeriesStructure([Measure(1,5)])
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
        if not membership(s2,m1):
            return False
    return True


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

    >>> s1 = TimeSeriesStructure([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> union(s2,s1) == s2
    True
    >>> union(s1,s2) == TimeSeriesStructure([Measure(1,2), Measure(3,2), Measure(2,1)])
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

    >>> s1 = TimeSeriesStructure([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> difference(s1,s1) == TimeSeriesStructure([])
    True
    >>> difference(s1,s2) == TimeSeriesStructure([Measure(2,1)])
    True
    >>> difference(s2,s1) == TimeSeriesStructure([Measure(2,2),Measure(3,2)])
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

    >>> s1 = TimeSeriesStructure([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> intersection(s1,s1) == s1
    True
    >>> intersection(s1,s2) == TimeSeriesStructure([Measure(1,2)])
    True
    >>> intersection(s2,s1) == intersection(s1,s2)
    True
    """
    return difference(s1,difference(s1,s2))



def symmetric_difference(s1, s2):
    """
    Operador de diferència simètrica. Sèrie temporal resultant
    de la diferènca simètrica d'`s1` amb la sèrie temporal `s2`.

    :param s1: 
    :param s2: 
    :type s1: :class:`TimeSeries`
    :type s2: :class:`TimeSeries`
    :returns: `s1 ⊖ s2`, s1 diferència simètrica s2
    :rtype: :class:`TimeSeries`

    >>> s1 = TimeSeriesStructure([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> symmetric_difference(s1,s1) == TimeSeriesStructure([])
    True
    >>> symmetric_difference(s1,s2) == TimeSeriesStructure([Measure(2,1),Measure(3,2)])
    True
    >>> symmetric_difference(s2,s1) == TimeSeriesStructure([Measure(2,2),Measure(3,2)])
    True
    """
    return union(difference(s1,s2),difference(s2,s1))








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

    >>> s = TimeSeriesStructure([Measure(1,2)])
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




def subset_temporal(s1,s2):
    """
    Operador de subconjunt temporal. Cert quan la sèrie temporal `s1` està
    inclosa temporalment a la sèrie temporal `s2`.

    Sempre es compleix que si s1.subset(s2)==True aleshores
    s1.subset_temporal(s2)==True

    :param s1: 
    :param s2: 
    :type s1: :class:`TimeSeries`
    :type s2: :class:`TimeSeries`
    :returns: `s1 ⊆ᵗ s2`, s1 inclosa temporalment a s2
    :rtype: bool

    >>> s1 = TimeSeriesStructure([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,1)])
    >>> s3 = TimeSeriesStructure([Measure(1,5)])
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
        if not membership_temporal(s2,m1):
            return False
    return True


def union_temporal(s1, s2):
    """
    Operador d'unió temporal. Sèrie temporal resultant d'unir
    temporalment la sèries temporal `s1` amb `s2`.

    :param s1: 
    :param s2: 
    :type s1: :class:`TimeSeries`
    :type s2: :class:`TimeSeries`
    :returns: `s1 ∪ᵗ s2`, s1 unió temporal s2
    :rtype: :class:`TimeSeries`

    >>> s1 = TimeSeriesStructure([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> union_temporal(s2,s1) ==  TimeSeriesStructure([Measure(3,2),Measure(1,2),])
    True
    >>> union_temporal(s1,s2) == union_temporal(s2,s1)
    True
    """
    s = s1.empty()
    for m1 in s1:
        if not membership_temporal(s2,m1):
            s.add(m1)
        elif membership(s2,m1):
            s.add(m1)

    for m2 in s2:
        if not membership_temporal(s1,m2):
            s.add(m2)
    return s

def difference_temporal(s1, s2):
    """
    Operador de diferència temporal. Sèrie temporal resultant de
    treure temporalment `s2` de la sèrie temporal `s1`.

    :param s1: 
    :param s2: 
    :type s1: :class:`TimeSeries`
    :type s2: :class:`TimeSeries`
    :returns: `s1 -ᵗ s2`, s1 diferència temporal s2
    :rtype: :class:`TimeSeries`

    >>> s1 = TimeSeriesStructure([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> difference_temporal(s1,s1) == difference(s1,s1)
    True
    >>> difference_temporal(s1,s2) == TimeSeriesStructure([])
    True
    >>> difference_temporal(s2,s1) == TimeSeriesStructure([Measure(3,2)])
    True
    """
    s = s1.empty()
    for m1 in s1:
        if not membership_temporal(s2,m1):
            s.add(m1)
    return s

def intersection_temporal(s1, s2):
    """
    Operador d'intersecció temporal. Sèrie temporal resultant
    d'interseccionar temporalment `s2` amb la sèrie temporal `s1`.

    :param s1: 
    :param s2: 
    :type s1: :class:`TimeSeries`
    :type s2: :class:`TimeSeries`
    :returns: `s1 ∩ᵗ s2`, s1 intersecció temporal s2
    :rtype: :class:`TimeSeries`

    >>> s1 = TimeSeriesStructure([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> intersection_temporal(s1,s1) == intersection(s1,s1)
    True
    >>> intersection_temporal(s1,s2) == TimeSeriesStructure([Measure(1,2),Measure(2,1)])
    True
    >>> intersection_temporal(s2,s1) == TimeSeriesStructure([Measure(1,2),Measure(2,2)])
    True
    """
    return difference_temporal(s1,difference_temporal(s1,s2))


def symmetric_difference_temporal(s1, s2):
    """
    Operador de diferència simètrica temporal. Sèrie temporal resultant
    de la diferènca simètrica temporal d'`s2` amb la sèrie temporal `s1`.

    :param s1: 
    :param s2: 
    :type s1: :class:`TimeSeries`
    :type s2: :class:`TimeSeries`
    :returns: `s1 ⊖ᵗ s2`, s1 diferència simètrica temporal s2
    :rtype: :class:`TimeSeries`

    >>> s1 = TimeSeriesStructure([Measure(1,2),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(3,2),Measure(1,2),Measure(2,2)])
    >>> symmetric_difference_temporal(s1,s1) == symmetric_difference(s1,s1)
    True
    >>> symmetric_difference_temporal(s1,s2) == TimeSeriesStructure([Measure(3,2)])
    True
    >>> symmetric_difference_temporal(s2,s1) == symmetric_difference_temporal(s1,s2)
    True
    """
    return union_temporal( difference_temporal(s1,s2), difference_temporal(s2,s1))












"""
Relational
==========
"""


def projection(self,A):
    """
    Operador de projecció. Conjunt resultant de seleccionar els
    atributs (columnes) `A` de la sèrie temporal.  

    :param A: exemple ['t','v']
    :type A: Iterable of attribute names
    :returns: `s{A}`, projecció de s en A
    :rtype: set 

    >>> s1 = TimeSeriesStructure([Measure(1,1),Measure(2,1)])
    >>> projection(TimeSeriesStructure([]), []) == set()
    True
    >>> projection(s1,[])  == set([])
    True
    >>> projection(s1,['t']) == set([1,2])
    True
    >>> projection(s1,['v']) == set([1])
    True
    >>> projection(s1,['t','v']) == set([(1,1),(2,1)])
    True
    >>> s2 = TimeSeriesStructure([Measure(1,[1,2]),Measure(2,[1,2])])
    >>> projection(s2,['t','v0'])  == set([(1,1),(2,1)])
    True
    >>> projection(s2,['t','v1'])  == set([(1,2),(2,2)])
    True
    >>> projection(s2,['t','v0','v1']) == set([(1,1,2),(2,1,2)])
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

    >>> s1 = TimeSeriesStructure([Measure(1,1),Measure(2,1),Measure(4,1)])
    >>> def t_gt_1(m):
    ...     return m.t > 1
    >>> selection(TimeSeriesStructure([]), t_gt_1) == set()
    True
    >>> selection(s1,t_gt_1) == TimeSeriesStructure([Measure(2,1),Measure(4,1)])
    True
    >>> selection(s1,lambda m: m.t > 1) == TimeSeriesStructure([Measure(2,1),Measure(4,1)])
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

    >>> s1 = TimeSeriesStructure([Measure(1,1),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(1,2),Measure(3,2)])
    >>> product(s1,s2) == set([(1,1,1,2),(1,1,3,2),(2,1,1,2),(2,1,3,2)])
    True
    >>> product(s2,s1) == set([(1,2,1,1),(3,2,1,1),(1,2,2,1),(3,2,2,1)])
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

    >>> s1 = TimeSeriesStructure([Measure(1,1),Measure(2,1)])
    >>> s2 = TimeSeriesStructure([Measure(1,2),Measure(3,2)])
    >>> join(s1,s2) == TimeSeriesStructure([Measure(1,(1,2))])
    True
    >>> join(s2,s1) == TimeSeriesStructure([Measure(1,(2,1))])
    True
    """
    s = self.empty()
    p = product(self,other)
    for (t1,v1,t2,v2) in p:
        if t1==t2:
            s.add(Measure(t1,(v1,v2)))
    return s


def mapp(self,f):
    """
    Operador de mapa. Sèrie temporal resultant de mapar amb la
    funció `f`.

    :param f: funció de mapatge, f(m)->m
    :type f: function of Measure returns Measure
    :returns: `map(s,f)`, mapa de f a s
    :rtype: :class:`TimeSeries`

    >>> s1 = TimeSeriesStructure([Measure(1,1),Measure(2,1)])
    >>> mapp(s1,lambda m: Measure(m.t,m.v*2)) == TimeSeriesStructure([Measure(1,2),Measure(2,2)])
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

    >>> s1 = TimeSeriesStructure([Measure(1,1),Measure(2,1)])
    >>> aggregate(s1,lambda mi,m: Measure(0,mi.v+m.v), Measure(0,0)) == Measure(0,2)
    True
    >>> aggregate(s1,lambda mi,m: Measure(0,mi.v+m.v)) == Measure(0,2)
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

    >>> s1 = TimeSeriesStructure([Measure(1,1),Measure(2,1)])
    >>> fold(s1,lambda s,m: s.union(TimeSeriesStructure([m]))) == s1
    True
    >>> from timeseries import TimeSeries
    >>> def tpredecessors(s):
    ...     si = mapp(s,lambda m: Measure(m.t,float("-inf")))
    ...     def f(si,m):
    ...         t = m.t
    ...         tp = selection(si,lambda m: m.t < t).sup().t
    ...         a = TimeSeries([Measure(t,tp)])
    ...         return union(a,si)
    ...     return fold(s,f,si)
    >>> tpredecessors(s1) == TimeSeriesStructure([Measure(1,float("-inf")),Measure(2,1)])
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

    >>> s1 = TimeSeriesStructure([Measure(1,1),Measure(2,1)])
    >>> orderfold(s1,lambda s,m: s.union(TimeSeriesStructure([m])),max) == s1
    True
    >>> orderfold(s1,lambda s,m: s.union(TimeSeriesStructure([m])),min) == s1
    True
    >>> orderfold(s1,lambda s,m: TimeSeriesStructure([m]),min) == TimeSeriesStructure([Measure(2,1)])
    True
    """
    if si is None:
        si = self.empty()

    if len(self) == 0:
        return si

    m0 = o(self)
    s0 = type(self)([m0])
    so = self - s0
    return orderfold(so,f,o,f(si,m0))        




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

    >>> s1 = TimeSeriesStructure([Measure(1,1),Measure(2,1),Measure(3,1)])
    >>> s2 = TimeSeriesStructure([Measure(1,2),Measure(3,2),Measure(5,2)])
    >>> op(s1,s2,lambda x,y: x+y) == TimeSeriesStructure([Measure(1,3),Measure(3,3)])
    True
    """
    return mapp(join(self,other) ,lambda m: Measure(m.t,f(m.v[0],m.v[1])))



