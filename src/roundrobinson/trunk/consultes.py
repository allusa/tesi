# -*- encoding: utf-8 -*-

"""
======================
Operacions de consulta
======================

:Abstract: Vegeu document principal `roundrobinson.py`
:Copyright: GPLv3

Implementació de les operacions de consulta
"""

import copy

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

def _sup(s):
    """
    Suprem d'un conjunt discret finit
    """
    if len(s):
        return max(s)
    return -float("inf")

def _inf(s):
    """
    Ínfim d'un conjunt discret finit
    """
    if len(s):
        return min(s)
    return float("inf")

def resolucio(s,i):
    """
    Selecció de la resolució de S en i amb representació zohe

    >>> s = _s1test()
    >>> resolucio(s, set([4]) )
    SerieTemporal([m(10,1), m(10,2), m(40,4)])
    >>> resolucio(s, set([6]) )
    SerieTemporal([m(10,1), m(10,2), m(40,5), m(inf,6)])
    >>> resolucio(s, set([0]) )
    SerieTemporal([m(10,0)])
    >>> resolucio(s, set([-2,2,4,10]) )
    SerieTemporal([m(10,-2), m(10,1), m(10,2), m(40,4), m(40,5), m(inf,10)])
    """
    tf = _sup(i)
    inext = i - set([tf])
    ta = _sup(inext)

    if len(i) == 0:
        return SerieTemporal()
    else:
        return resolucio(s,inext).union( seleccio(s,(ta,tf)) )
        


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


def fusio(s1,s2):
    """
    Fusió temporal de s1 i s2 amb representació zohe

    >>> s1 = _s1test()
    >>> s2 = _s2test()
    >>> fusio(s1,s2)
    SerieTemporal([m((10, 60),0), m((10, 70),1), m((10, 70),2), m((40, 70),4), m((40, 50),5), m((inf, 30),10)])
    >>> fusio(s2,s1)
    SerieTemporal([m((60, 10),0), m((70, 10),1), m((70, 10),2), m((70, 40),4), m((50, 40),5), m((30, inf),10)])
    """
    t = set()
    for m1 in s1:
        t1 = m1.t
        t.add(t1)
    for m2 in s2:
        t2 = m2.t
        t.add(t2)
    
    rs1 = resolucio(s1,t)
    rs2 = resolucio(s2,t)

    s = SerieTemporal()
    for tp in t:
        v1 = rs1[tp].v
        v2 = rs2[tp].v
        mp = Mesura( (v1,v2), tp)
        s.add(mp)
    return s



def opera(s,f):
    """
    Aplica una funció f( (m0,m1,...,mn) ,t) a una sèrie temporal 
    """
    ss = copy.copy(s)
    for m in ss:
        m.v = f(m.v,m.t)
    return ss

def mitjana(v,t):
    """
    Calcula la mitjana per cada mesura d'una sèrie temporal multivaluada

    >>> s1 = _s1test()
    >>> s2 = _s2test()   
    >>> opera(s1,mitjana)
    SerieTemporal([m(10,1), m(10,2), m(40,5)])
    >>> opera(fusio(s1,s2),mitjana)
    SerieTemporal([m(35.0,0), m(40.0,1), m(40.0,2), m(55.0,4), m(45.0,5), m(inf,10)])
    """
    try:
        len(v)
    except TypeError:
        return v 
    else:
        return sum(v) / float(len(v))
