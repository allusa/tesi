# -*- encoding: utf-8 -*-
"""
==========================
Sèries temporals i Mesures
==========================

:Abstract: Vegeu document principal `roundrobinson.py`
:Copyright: GPLv3

Implementació de les definicions de Mesura i Sèrie Temporal.
"""

def _s1test():
    """
    Retorna una sèrie temporal de prova
    """
    m1 = Mesura(10,1)
    m2 = Mesura(10,2)
    m3 = Mesura(40,5)

    s = SerieTemporal() 
    s.add(m1)
    s.add(m2)
    s.add(m3)

    return s


class Mesura(object):
    """
    Mesura m = (v,t) on v és el valor en el temps t. El temps implementat com a temps relatiu. 

    :ivar v: m.v correspon a V(m) 
    :ivar t: m.t correspon a T(m)

    >>> m1 = Mesura(10,1)
    >>> m2 = Mesura(10,2)
    >>> m1
    m(10,1)
    >>>
    >>> m1 > m2
    False
    >>> m2 > m1
    True
    >>> m1 < m2
    True
    >>> m2 < m1
    False
    >>> m1 == m2
    False
    >>> m1 ==  Mesura(20,1)
    True
    """
    def __init__(self,v,t):
        """
        Constructor d'una mesura
        """        
        self.v = v
        self.t = t

    def __gt__(self,other):
        """
        Relació d'ordre induïda pel temps
        """
        return self.t > other.t 
    
    def __eq__(self,other):        
        """
        Relació d'ordre induïda pel temps
        """
        return isinstance(other,Mesura) and self.t == other.t

    def __ne__(self,other):
        """
        Relació d'ordre induïda pel temps
        """
        return not self == other

    def __hash__(self):
        """
        Retorna el hash d'una mesura, necessari per poder pertànyer a objectes colleccions com per exemple els sets
        """
        return hash(self.t)
    
    def __repr__(self):
        return 'm({0},{1})'.format(self.v,self.t)

class SerieTemporal(set):
    """
    Sèrie temporal s = {m0,...,mk} com una seqüència de mesures ordenades en el temps

    És una subclasse de set. De la definició de set a Python:

     A set is an unordered collection with no duplicate elements.
     Basic uses include membership testing and eliminating duplicate entries. Set objects also support mathematical operations like union, intersection, difference, and symmetric difference.

    Un `set` és un conjunt d'elements no repetits però sense ordre. Els tipus amb ordre a Python s'anomenen `sequence` però no són conjunts.  Oficialment a Python (v2.7) no hi ha un `OrderedSet`.


    >>> m1 = Mesura(10,1)
    >>> m2 = Mesura(10,2)
    >>> m3 = Mesura(20,1)
    >>> s = SerieTemporal()
    >>> 
    >>> s.add(m1)
    >>> s.add(m2)
    >>> s.add(m3) #repetit, no s'afegeix
    >>> s
    SerieTemporal([m(10,1), m(10,2)])
    >>> min(s)
    m(10,1)
    >>> max(s)
    m(10,2)
    >>> s[2]
    m(10,2)
    >>>
    >>> m4 = Mesura(40,5)
    >>> s.add(m4)
    >>> s[1:4]
    SerieTemporal([m(10,2)])
    >>> s[0:]
    SerieTemporal([m(10,1), m(10,2), m(40,5)])
    >>> 
    >>> s[1:4].issubset(s)
    True
    >>> s2 = SerieTemporal()
    >>> m5 = Mesura(34,6)
    >>> s2.add(m4)
    >>> s2.add(m5)
    >>> s2.issubset(s)
    False
    >>> s.union(s2) # s | s2
    SerieTemporal([m(10,1), m(10,2), m(40,5), m(34,6)])
    >>> s.intersection(s2) # s & s2
    SerieTemporal([m(40,5)])
    >>> s.difference(s2) # s - s2
    SerieTemporal([m(10,1), m(10,2)])
    >>> s.symmetric_difference(s2) # s ^ s2
    SerieTemporal([m(10,1), m(10,2), m(34,6)])
    >>>
    >>> s.seg(m1)
    m(10,2)
    >>> s.ant(m2)
    m(10,1)
    """
    def __getitem__(self,key):
        """
        Definició d'element i interval d'elements en una sèrie temporal. Definició contínua per l'esquerra:

        `s[r:t]` correspon a la definició S(r,t] on r i t són dos temps. `s[r:]`correspon a la definició S(r,infinit), així com `s[:t]`correspon a S(-infinit,t] i `s[:]`correspon a S(-infinit,infinit).


        Per implementació a Python cal definir l'element `s[i]`, el qual es fa correspondre amb m in S: T(m) = i

        :param key: Element S(i) o interval d'elements S(r:t) 
        :type key: int or slice

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

        >>> s = _s1test() 
        >>> s.sup()
        m(40,5)
        >>> s2 = SerieTemporal()
        >>> s2.sup()
        m(inf,-inf)
        """
        if len(self) == 0:
            return Mesura(float("inf"),-float("inf"))
        else:
            return max(self)

    def inf(self):
        """
        Ínfim de la sèrie temporal

        :returns: La mesura ínfima de S
        :rtype: mesura

        >>> s = _s1test() 
        >>> s.inf()
        m(10,1)
        >>> s2 = SerieTemporal()
        >>> s2.inf()
        m(inf,inf)
        """
        if len(self) == 0:
            return Mesura(float("inf"),+float("inf"))
        else:
            return min(self)


    def seg(self,m):
        """ 
        Mesura següent. Successor de m en S.

        :type m: mesura
        :returns: La mesura següent a m
        :rtype: mesura
        
        >>> m1 = Mesura(10,1)
        >>> m2 = Mesura(10,2)
        >>> m3 = Mesura(20,5)
        >>> s = SerieTemporal()
        >>> s.add(m1)
        >>> s.add(m2)
        >>> s.add(m3)
        >>>
        >>> s.seg(m2)
        m(20,5)
        >>> s.seg(max(s))
        m(inf,inf)
        >>> mi = Mesura(float("inf"),-float("inf"))
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
        Mesura anterior. Predecessor de m en S.

        :type m: mesura
        :returns: La mesura anterior a m
        :rtype: mesura
        
        >>> m1 = Mesura(10,1)
        >>> m2 = Mesura(10,2)
        >>> m3 = Mesura(20,5)
        >>> s = SerieTemporal()
        >>> s.add(m1)
        >>> s.add(m2)
        >>> s.add(m3)
        >>>
        >>> s.ant(m2)
        m(10,1)
        >>> s.ant(min(s))
        m(inf,-inf)
        >>> mi = Mesura(float("inf"),float("inf"))
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
