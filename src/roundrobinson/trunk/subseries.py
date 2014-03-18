# -*- encoding: utf-8 -*-

"""
==================
Subsèrie Resolució
==================

:Abstract: Vegeu document principal `roundrobinson.py`
:Copyright: GPLv3

Implementació de les definicions de Buffer, Disc i SubsèrieResolució.
"""


from pytsms import Measure, TimeSeries
               
            
class Buffer(object):
    """
    Buffer B = (S,tau,delta,f) on S és una sèrie temporal, tau el darrer temps de consolidació, delta el pas de consolidació i f un interpolador

    :param delta: El pas de consolidació
    :param f: L'interpolador associat al buffer
    :param tau: El temps de consolidació inicial, per defecte zero (enter)

    >>> m1 = Measure(1,10)
    >>> m2 = Measure(2,10)
    >>> m3 = Measure(5,40)
    >>> 
    >>> def mitjana(s,i):
    ...     sp = s.interval_open_left(i[0],i[1])
    ...     v = sp.aggregate(lambda mi,m: Measure(mi.t+1, mi.v+m.v), Measure(0,0))
    ...     return Measure(i[1], v.v / v.t )
    >>> B = Buffer(5,mitjana)
    >>> 
    >>> B.consolidable()
    False
    >>> B.add(m1)
    >>> B.consolidable()
    False
    >>> B.add(m2)
    >>> B.consolidable()
    False
    >>> B.add(m3)
    >>> B.consolidable()
    True
    >>> B.consolidate() == Measure(5,20)
    True
    >>> B.s == TimeSeries() and B.delta == 5 and B.tau == 5
    True
    """
    def __init__(self,delta,f,tau=0):
        """
        Constructor d'un Buffer buit
        """
        self.s = TimeSeries()
        self.delta = delta
        self.f = f
        self.tau = tau

    def __eq__(self,other):
        """
        Relació d'igualtat
        """
        return self.s == other.s and self.schema_eq(other)


    def _f_eq(self,other):
        """
        Igualtat entre agregadors
        """
        if self.f == other.f:
            return True
        return self.f.__code__ == other.f.__code__
        
        
    def schema_eq(self,other):
        """
        Relació d'igualtat d'esquema multiresolució
        """
        return self.delta == other.delta and self._f_eq(other) and self.tau == other.tau



    def add(self,m):
        """
        Definició de l'operació afegeix
        """
        self.s.add(m)


    def consolidation_times(self,n):
        """
        Retorna els n instants de temps de consolidació futurs

        >>> m1 = Measure(1,10); m2 = Measure(2,10); m3 = Measure(5,40)
        >>> B = Buffer(5,lambda s,i: max(s),0)
        >>> B.consolidation_times(5)
        [0, 5, 10, 15, 20]
        """
        return [self.tau + i*self.delta for i in range(n)]




    def consolidable(self):
        """
        Definició del predicat consolidable
        """
        if len(self.s) < 1:
            return False
        m = self.s.sup()
        return m.t >= (self.tau + self.delta)



    def _rm_olds(self,t0,tf):
        """
        Elimina les mesures velles del buffer que ja no són
        necessàries sabent que s'ha consolidat l'interval [t0,tf]
        """
        self.s = self.s[tf::'l']


    def consolidate(self):
        """
        Definició de l'operació consolida
        """
        noutau = self.tau + self.delta
        
        interval = (self.tau,noutau)
        interpola = self.f(self.s, interval)

        self._rm_olds(self.tau,noutau)

        self.tau = noutau
 
        return interpola


    def __repr__(self):
        return 'Buffer({0},delta= {1},f= {2},tau= {3})'.format(self.s,self.delta,self.f,self.tau)




class Disc(object):
    """
    Disc D = (S,k) on S és una sèrie temporal i k és el cardinal màxim de S

    :param k: El cardinal màxim del disc

    >>> m1 = Measure(1,10)
    >>> m2 = Measure(2,10)
    >>> m3 = Measure(5,40)
    >>> D = Disc(2)
    >>> 
    >>> D.add(m1)
    >>> D.s == TimeSeries([Measure(1,10)])
    True
    >>> D.add(m2)
    >>> D.s == TimeSeries([Measure(1,10), Measure(2,10)])
    True
    >>> D.add(m3)
    >>> D.s == TimeSeries([Measure(2,10), Measure(5,40)])
    True
    >>> D.k == 2
    True
    """
    def __init__(self,k):
        """
        Constructor d'un Disc buit
        """
        self.s = TimeSeries()
        self.k = k

    def __eq__(self,other):
        """
        Relació d'igualtat
        """
        return self.s == other.s and self.schema_eq(other)

    def schema_eq(self,other):
        """
        Relació d'igualtat d'esquema multiresolució
        """
        return self.k == other.k


    def add(self,m):
        """
        Definició de l'operació `afegeix`
        """
        if len(self.s) < self.k:
            self.s.add(m)
        else:
            #smin = self.s.empty()
            #smin.add( min(self.s) )            
            #self.s = self.s - smin
            self.s.discard(min(self.s))

            self.s.add(m)

    def __repr__(self):
        return 'Disc({0}, |{1}|)'.format(self.s,self.k)


class ResolutionSubseries(object):
    """
    Disc Resolucio R = (B,D) on B és un buffer i D és un disc
    
    :param delta: pas de consolidació
    :param k: cardinal màxim del disc
    :param f: funció d'interpolació
    :param tau: El temps de consolidació inicial, per defecte zero (enter)

    >>> m1 = Measure(1,10)
    >>> m2 = Measure(2,10)
    >>> m3 = Measure(5,40) 
    >>> def mitjana(s,i):
    ...     sp = s.interval_open_left(i[0],i[1])
    ...     v = sp.aggregate(lambda mi,m: Measure(mi.t+1, mi.v+m.v), Measure(0,0))
    ...     return Measure(i[1], v.v / v.t )
    >>> R = ResolutionSubseries(5,2,mitjana,0)
    >>>
    >>> R.add(m1)
    >>> R.consolidable()
    False
    >>> R.add(m2)
    >>> R.consolidable()
    False
    >>> R.add(m3)
    >>> R.consolidable()
    True
    >>> R.consolidate()
    >>> R.B.s == TimeSeries() and R.B.delta == 5 and R.B.tau == 5
    True
    >>> R.D.s == TimeSeries([Measure(5,20)]) and R.D.k == 2
    True
    """
    def __init__(self,delta,k,f,tau=0):
        """
        Constructor d'un Disc Resolucio buit
        """
        self.B = Buffer(delta,f,tau)
        self.D = Disc(k)

    def __gt__(self,other):
        """
        Relació d'ordre induïda pel temps de consolidació del Buffer
        Definint l'ordre, després es pot ordenar un conjunt de discs
        resolució mitjançant la funció sorted(mrd)
        """
        return self.B.delta > other.B.delta

    def __eq__(self,other):
        """
        Relació d'igualtat
        """
        return self.B == other.B and self.D == other.D

    def schema_eq(self,other):
        """
        Relació d'igualtat d'esquema multiresolució
        """
        return self.B.schema_eq(other.B) and self.D.schema_eq(other.D)



    def __repr__(self):
        return 'RD:{0},{1}'.format(self.B,self.D)




    def add(self,m):
        """
        Definició de l'operació `afegeix`
        """
        self.B.add(m)

    def consolidable(self):
        """
        Definició del predicat `consolidable`
        """
        return self.B.consolidable()

    def consolidate(self):
        """
        Definició de l'operació `consolida`
        """
        m = self.B.consolidate()
        self.D.add(m)


    def delta(self):
        return self.B.delta

    def tau(self):
        return self.B.tau

    def f(self):
        return self.B.f

    def k(self):
        return self.D.k

    def sb(self):
        return self.B.s

    def sd(self):
        return self.D.s

