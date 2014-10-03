# -*- encoding: utf-8 -*-

"""
=============
RoundRobinson
=============

:Author: Aleix Llusà Serra
:Contact: aleix@dipse.upc.edu
:Version: 0.1a
:Date: 	2011-06-04
:Abstract: Implementació en Python d'un SGBD Round Robin (RRD)
:Copyright: GPLv3

Implementació en Python d'un SGBD Round Robin (RRD). És la implementació de referència del model de dades Round Robin descrit al capítol 6 de la tesi de màster..

Amb el suport de la Universitat Politècnica de Catalunya (UPC).
"""


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
    """
    def __getitem__(self,key):
        """
        Definició d'element i interval d'elements en una sèrie temporal.

        `s[r:t]` correspon a la definició S(r,t] on r i t són dos temps. `s[r:]`correspon a la definició S(r,infinit), així com `s[:t]`correspon a S(-infinit,t] i `s[:]`correspon a S(-infinit,infinit).


        Per implementació a Python cal definir l'element `s[i]`, el qual es fa correspondre amb m in S: T(m) = i

        :param key: Element S(i) o interval d'elements S(r:t) 
        :type key: int or slice
        """
        #mesura màxima i mínima de la sèrie temporal
        minm = min(self)
        maxm = max(self)

        #interval d'elements
        if isinstance(key,slice):    
            l = key.start
            g = key.stop
            p = key.step
 
            #Per definició, S(r,infinit) és S(r,T(max(S))]
            if g is None:
                g = maxm.t

            s = SerieTemporal()
            for m in self:
                if m.t > l and m.t <= g:
                    s.add(m)
            return s

        #element
        else:
            l = key
            g = key

            if l < minm.t or g > maxm.t:
                raise IndexError
            for m in self:
                if m.t == key:
                    return m
          
        raise KeyError
                
            
class Buffer(object):
    """
    Buffer B = (S,tau,delta,f) on S és una sèrie temporal, tau el darrer temps de consolidació, delta el pas de consolidació i f un interpolador

    :param delta: El pas de consolidació
    :param f: L'interpolador associat al buffer

    >>> m1 = Mesura(10,1)
    >>> m2 = Mesura(10,2)
    >>> m3 = Mesura(40,5)
    >>> 
    >>> def mitjana(s,i):
    ...     return Mesura((10+10+40) / 3 , i[1])
    >>> B = Buffer(5,mitjana)
    >>> 
    >>> B.consolidable()
    False
    >>> B.afegeix(m1)
    >>> B.consolidable()
    False
    >>> B.afegeix(m2)
    >>> B.consolidable()
    False
    >>> B.afegeix(m3)
    >>> B.consolidable()
    True
    >>> B.consolida()
    m(20,5)
    >>> B
    Buffer(SerieTemporal([]),5,5)
    """
    def __init__(self,delta,f):
        """
        Constructor d'un Buffer buit
        """
        self.s = SerieTemporal()
        self.tau = 0
        self.delta = delta
        self.f = f

    def afegeix(self,m):
        """
        Definició de l'operació afegeix
        """
        self.s.add(m)

    def consolidable(self):
        """
        Definició del predicat consolidable
        """
        if self.s:
            m = max(self.s)
            return m.t >= (self.tau + self.delta)
        return False

    def consolida(self):
        """
        Definició de l'operació consolida
        """
        noutau = self.tau + self.delta
        
        interval = (self.tau,noutau)
        interpola = self.f(self.s, interval)

        self.s = self.s[noutau:]
        self.tau = noutau
        self.delta = self.delta

        return interpola


    def __repr__(self):
        return 'Buffer({0},{1},{2})'.format(self.s,self.tau,self.delta)




class Disc(object):
    """
    Disc D = (S,k) on S és una sèrie temporal i k és el cardinal màxim de S

    :param k: El cardinal màxim del disc

    >>> m1 = Mesura(10,1)
    >>> m2 = Mesura(10,2)
    >>> m3 = Mesura(40,5)
    >>> D = Disc(2)
    >>> 
    >>> D.afegeix(m1)
    >>> D.s
    SerieTemporal([m(10,1)])
    >>> D.afegeix(m2)
    >>> D.s
    SerieTemporal([m(10,1), m(10,2)])
    >>> D.afegeix(m3)
    >>> D.s
    SerieTemporal([m(10,2), m(40,5)])
    """
    def __init__(self,k):
        """
        Constructor d'un Disc buit
        """
        self.s = SerieTemporal()
        self.k = k

    def afegeix(self,m):
        """
        Definició de l'operació `afegeix`
        """
        if len(self.s) < self.k:
            self.s.add(m)
        else:
            smin = SerieTemporal()
            smin.add( min(self.s) )
            
            self.s -= smin
            self.s.add(m)

    def __repr__(self):
        return 'Disc({0}, |{1}|)'.format(self.s,self.k)


class DiscRoundRobin(object):
    """
    Disc Round Robin R = (B,D) on B és un buffer i D és un disc
    
    :param delta: pas de consolidació
    :param k: cardinal màxim del disc
    :param f: funció d'interpolació

    >>> m1 = Mesura(10,1)
    >>> m2 = Mesura(10,2)
    >>> m3 = Mesura(40,5) 
    >>> def mitjana(s,i):
    ...     return Mesura((10+10+40) / 3 , i[1])
    >>> R = DiscRoundRobin(5,2,mitjana)
    >>>
    >>> R.afegeix(m1)
    >>> R.consolidable()
    False
    >>> R.afegeix(m2)
    >>> R.consolidable()
    False
    >>> R.afegeix(m3)
    >>> R.consolidable()
    True
    >>> R.consolida()
    >>> R
    DRR:Buffer(SerieTemporal([]),5,5),Disc(SerieTemporal([m(20,5)]), |2|)
    """
    def __init__(self,delta,k,f):
        """
        Constructor d'un Disc Round Robin buit
        """
        self.B = Buffer(delta,f)
        self.D = Disc(k)

    def afegeix(self,m):
        """
        Definició de l'operació `afegeix`
        """
        self.B.afegeix(m)

    def consolidable(self):
        """
        Definició del predicat `consolidable`
        """
        return self.B.consolidable()

    def consolida(self):
        """
        Definició de l'operació `consolida`
        """
        m = self.B.consolida()
        self.D.afegeix(m)

    def __repr__(self):
        return 'DRR:{0},{1}'.format(self.B,self.D)



class RRD(object):
    """
    M = (B,A) una base de dades Round Robin on B és un buffer i A és un conjunt de discs Round Robin

    >>> M = RRD(5,mitjana)
    >>> M.afegeix_disc(10,2,mitjana)
    >>>
    >>> m1 = Mesura(10,1)
    >>> m2 = Mesura(10,2)
    >>> m3 = Mesura(40,5) 
    >>> m4 = Mesura(50,10)
    >>>
    >>> M.update(m1)
    >>> M.consolidable()
    False
    >>> M.update(m2)
    >>> M.consolidable()
    False
    >>> M.update(m3)
    >>> M.consolidable()
    True
    >>> M.update(m4)
    >>> M.consolidable()
    True
    >>> M.consolidar()
    >>> M.rodable()
    False
    >>> M.consolidable()
    True
    >>> M.consolidar()
    >>> M.rodable()
    True
    >>> M.consolidable()
    False
    >>> M.roda()
    >>> M.rodable()
    False
    >>> M.consolidable()
    False
    >>> M.A
    [DRR:Buffer(SerieTemporal([]),10,10),Disc(SerieTemporal([m(35.0,10)]), |2|)]
    """

    def __init__(self,delta,f):
        self.B = Buffer(delta,f)
        self.A = []

    def afegeix_disc(self,delta,k,f):
        self.A.append( DiscRoundRobin(delta,k,f) )

    def update(self,m):
        self.B.afegeix(m)

    def consolidable(self):
        return self.B.consolidable()

    def consolidar(self):
        m = self.B.consolida()
        for R in self.A:
            R.afegeix(m)


    def rodable(self):
        for R in self.A:
            if R.consolidable():
                return True
        return False

    def roda(self):
        for R in self.A:
            if R.consolidable():
                R.consolida()


#interpoladors
def mitjana(s,i):
    """
    >>> m1 = Mesura(10,1)
    >>> m2 = Mesura(10,2)
    >>> m3 = Mesura(40,5)
    >>> s = SerieTemporal()
    >>> s.add(m1); s.add(m2); s.add(m3)
    >>>
    >>> mitjana(s,(0,5))
    m(20.0,5)
    """
    sp = s[i[0]:i[1]]
    v = 0
    for m in sp:
        v += m.v 
    v /= float(len(sp))
    return Mesura(v,i[1])

    
