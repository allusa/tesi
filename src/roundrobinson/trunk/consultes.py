# -*- encoding: utf-8 -*-

"""
======================
Operacions de consulta
======================

:Abstract: Vegeu document principal `roundrobinson.py`
:Copyright: GPLv3

Implementació de les operacions de consulta
"""

from serietemporal import Mesura,SerieTemporal
from roundrobinson import RRD, DiscRoundRobin
from interpoladors import mitjana

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

def _s2test():
    """
    Retorna una sèrie temporal de prova
    """
    m1 = Mesura(60,0)
    m2 = Mesura(70,4)
    m3 = Mesura(50,5)
    m4 = Mesura(30,10)

    s = SerieTemporal() 
    s.add(m1)
    s.add(m2)
    s.add(m3)
    s.add(m4)

    return s

def _s3test():
    """
    Retorna una sèrie temporal de prova
    """
    m1 = Mesura(40,5)

    s = SerieTemporal() 
    s.add(m1)

    return s

def _rrdtest():
    """
    Retorna una base de dades Round Robin de prova
    """
    M = RRD()

    r1 = DiscRoundRobin(2,10,mitjana)
    r1.D.s = _s1test()

    r2 = DiscRoundRobin(5,10,mitjana)
    r2.D.s = _s2test()

    r3 = DiscRoundRobin(10,10,mitjana)
    r3.D.s = _s3test()
    
    M.add(r1)
    M.add(r2)
    M.add(r3)

    return M

def seleccio(s,i):
    """
    Selecció temporal de `s` en `i` amb representació zohe.

    >>> s = _s1test()
    >>> seleccio(s,(0,5))
    SerieTemporal([m(10,1), m(10,2), m(40,5)])
    >>> seleccio(s,(0,4))
    SerieTemporal([m(10,1), m(10,2), m(40,4)])
    >>> seleccio(s,(1,5))
    SerieTemporal([m(10,2), m(40,5)])
    >>> seleccio(s,(-1,0))
    SerieTemporal([m(10,0)])
    >>> seleccio(s,(1,6))
    SerieTemporal([m(10,2), m(40,5), m(inf,6)])
    >>>
    >>> s2 = SerieTemporal()
    >>> seleccio(s2,(0,5))
    SerieTemporal([m(inf,5)])
    """
    t0,tf = i

    v = (s-s["-i":tf]).inf().v
    m = Mesura(v,tf)
    sm = SerieTemporal(); sm.add(m)

    return (s.union(sm))[t0:tf]


def unio(s1,s2):
    """
    Unió temporal de `s1` i `s2` amb representació zohe

    >>> s1 = _s1test()
    >>> s2 = _s2test()
    >>> s3 = _s3test()
    >>> unio(s1,s2)
    SerieTemporal([m(60,0), m(10,1), m(10,2), m(40,5), m(30,10)])
    >>> unio(s2,s1)
    SerieTemporal([m(60,0), m(70,4), m(50,5), m(30,10)])
    >>> unio(s1,s1) == s1
    True
    >>> unio(unio(s1,s2),s3) == unio(s1,unio(s2,s3))
    True
    >>> unio(s1,SerieTemporal()) == s1
    True
    >>> unio(SerieTemporal(),s1) == s1
    True
    """
    t1 = s1.inf().t
    t2 = s1.sup().t

    return s1.union( s2 - seleccio(s2,(t1,t2)) )



def consulta(m):
    """
    Consulta temporal de la base de dades Round Robin `m` en
    l'interpolador `f` amb representació zohe.

    >>> M = _rrdtest()
    >>> consulta(M)
    SerieTemporal([m(60,0), m(10,1), m(10,2), m(40,5), m(30,10)])
    >>> consulta(RRD())
    SerieTemporal([])
    """
    if len(m) == 0:
        return SerieTemporal()

    delta0 = float("inf")
    for r in m:
        b = r.B
        d = r.D
        delta = b.delta

        if delta < delta0:
            delta0 = delta
            sd0 = d.s
            r0 = r 

    mr0 = RRD(); mr0.add(r0)
    return unio(sd0, consulta(m-mr0) )

    
        
    


