# -*- encoding: utf-8 -*-

"""
=============
RoundRobinson
=============

:Author: Aleix Llusà Serra
:Contact: aleix@dipse.upc.edu
:Version: 0.1b-dev
:Date: 	2011-09-20
:Abstract: Implementació en Python d'un SGBD Round Robin (RRD)
:Copyright: GPLv3

Implementació en Python d'un SGBD Round Robin (RRD). És la implementació de referència del model de dades Round Robin descrit al capítol 6 de la tesi de màster..

Amb el suport de la Universitat Politècnica de Catalunya (UPC).
"""


from serietemporal import Mesura, SerieTemporal
from interpoladors import mitjana, area
                
            
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



class RRD(set):
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
    >>> M
    RRD([DRR:Buffer(SerieTemporal([]),10,10),Disc(SerieTemporal([m(35.0,10)]), |2|)])
    """

    def __init__(self,delta=None,f=None):
        if delta and f:
            self.B = Buffer(delta,f)
        set.__init__(self)

    def afegeix_disc(self,delta,k,f):
        self.add( DiscRoundRobin(delta,k,f) )

    def update(self,m):
        self.B.afegeix(m)

    def consolidable(self):
        return self.B.consolidable()

    def consolidar(self):
        m = self.B.consolida()
        for R in self:
            R.afegeix(m)


    def rodable(self):
        for R in self:
            if R.consolidable():
                return True
        return False

    def roda(self):
        for R in self:
            if R.consolidable():
                R.consolida()



    
