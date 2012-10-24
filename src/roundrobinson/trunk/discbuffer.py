# -*- encoding: utf-8 -*-

"""
===============
Buffers i Discs
===============

:Abstract: Vegeu document principal `roundrobinson.py`
:Copyright: GPLv3

Implementació de les definicions de Buffer, Disc i DiscResolució.
"""


from serietemporal import Mesura, SerieTemporal
               
            
class Buffer(object):
    """
    Buffer B = (S,tau,delta,f) on S és una sèrie temporal, tau el darrer temps de consolidació, delta el pas de consolidació i f un interpolador

    :param delta: El pas de consolidació
    :param f: L'interpolador associat al buffer
    :param tau: El temps de consolidació inicial, per defecte zero (enter)

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
    def __init__(self,delta,f,tau=0):
        """
        Constructor d'un Buffer buit
        """
        self.s = SerieTemporal()
        self.delta = delta
        self.f = f
        if tau is None:
            tau = 0
        self.tau = tau


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


class ResolutionDisc(object):
    """
    Disc Resolucio R = (B,D) on B és un buffer i D és un disc
    
    :param delta: pas de consolidació
    :param k: cardinal màxim del disc
    :param f: funció d'interpolació
    :param tau: El temps de consolidació inicial, per defecte zero (enter)

    >>> m1 = Mesura(10,1)
    >>> m2 = Mesura(10,2)
    >>> m3 = Mesura(40,5) 
    >>> def mitjana(s,i):
    ...     return Mesura((10+10+40) / 3 , i[1])
    >>> R = ResolutionDisc(5,2,mitjana)
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
    RD:Buffer(SerieTemporal([]),5,5),Disc(SerieTemporal([m(20,5)]), |2|)
    """
    def __init__(self,delta,k,f,tau=None):
        """
        Constructor d'un Disc Resolucio buit
        """
        self.B = Buffer(delta,f,tau)
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
        return 'RD:{0},{1}'.format(self.B,self.D)



    def __gt__(self,other):
        """
        Relació d'ordre induïda pel temps de consolidació del Buffer
        Definint l'ordre, després es pot ordenar un conjunt de discs
        resolució mitjançant la funció sorted(mrd)
        """
        return self.B.delta > other.B.delta
