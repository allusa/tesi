# -*- encoding: utf-8 -*-

"""
=============
Interpoladors
=============

:Abstract: Vegeu document principal `roundrobinson.py`
:Copyright: GPLv3

Implementació dels interpoladors
"""

import math

from pytsms import Measure, TimeSeries
from pytsms.representation import Zohe


def mean(s,i):
    """
    Agregador mitjana aritmètica discreta amb T(m')=tf

    >>> m1 = Measure(1,10); m2 = Measure(2,10); m3 = Measure(5,40)
    >>> s = TimeSeries([m1,m2,m3])
    >>> mean(s,(0,5)) == Measure(5,20)
    True
    >>> mean(s,(0,6)) == Measure(6,20)
    True
    """
    t0,tf = i
    sp = s.interval_open_left(t0,tf)
    v = sp.aggregate(lambda mi,m: Measure(mi.t+1, mi.v+m.v), Measure(0,0))
    if v.t == 0:
        return Measure(tf,float("inf"))
    return Measure(tf, v.v / float(v.t) )


def maximum(s,i):
    """
    Agregador màxim discret amb T(m')=tf

    >>> m1 = Measure(1,10); m2 = Measure(2,40); m3 = Measure(5,20)
    >>> s = TimeSeries([m1,m2,m3])
    >>> maximum(s,(0,5)) == Measure(5,40)
    True
    >>> maximum(s,(0,6)) == Measure(6,40)
    True
    """
    t0,tf = i
    sp = s.interval_open_left(t0,tf)
    v = max(sp.projection(['v']))
    return Measure(tf,v)

def last(s,i):
    """
    Agregador darrer discret amb T(m')=tf

    >>> m1 = Measure(1,10); m2 = Measure(2,40); m3 = Measure(5,20)
    >>> s = TimeSeries([m1,m2,m3])
    >>> last(s,(0,5)) == Measure(5,20)
    True
    >>> last(s,(0,6)) == Measure(6,20)
    True
    """
    t0,tf = i
    sp = s.interval_open_left(t0,tf)
    v = max(sp).v
    return Measure(tf,v)


    
def area_zohe(s,i):
    """
    Agregador àrea ZOHE

    >>> m1 = Measure(1,10); m2 = Measure(2,10); m3 = Measure(5,40)
    >>> s = TimeSeries([m1,m2,m3])
    >>> area_zohe(s,(1,5)) == Measure(5,130)
    True
    >>> area_zohe(s,(0,5)) == Measure(5,140)
    True
    >>> area_zohe(s,(-1,5)) == Measure(5,150)
    True
    >>> area_zohe(s,(0,4)) == Measure(4,100)
    True
    >>> area_zohe(s,(0.5,3.5)) == Measure(3.5,75)
    True
    >>> area_zohe(s,(0,6)) == Measure(6,float("inf"))
    True
    >>> area_zohe(s,(0,1)) == Measure(1,10)
    True
    >>> area_zohe(s,(-1,0)) == Measure(0,10)
    True
    """
    t0,tf = i

    sp = s.interval_temporal(t0,tf,Zohe)
    o = min(sp)
    spp = sp - TimeSeries([o])
    
    vp = (o.t - t0)*o.v
    vp += reduce(lambda mi,m: mi+(m.t-s.prev(m).t)*m.v,spp,0)

    return Measure(tf,vp)  


def mean_zohe(s,i):
    """
    Agregador mitjana ZOHE

    >>> m1 = Measure(1,10); m2 = Measure(2,10); m3 = Measure(5,40)
    >>> s = TimeSeries([m1,m2,m3])
    >>> mean_zohe(s,(1,5.0)) == Measure(5,32.5)
    True
    >>> mean_zohe(s,(0,5)) == Measure(5,28)
    True
    >>> mean_zohe(s,(-1,5)) == Measure(5,25)
    True
    >>> mean_zohe(s,(0.5,3.5)) == Measure(3.5,25)
    True
    >>> mean_zohe(s,(0,6)) == Measure(6,float("inf"))
    True
    >>> mean_zohe(s,(0,1)) == Measure(1,10)
    True
    """
    t0,tf = i
    area = area_zohe(s,i).v
    v = area/(tf-t0)
    return Measure(tf,v)


def maximum_zohe(s,i):
    """
    Agregador màxim ZOHE

    >>> m1 = Measure(1,10); m2 = Measure(2,40); m3 = Measure(5,20)
    >>> s = TimeSeries([m1,m2,m3])
    >>> maximum_zohe(s,(1,5)) == Measure(5,40)
    True
    >>> maximum_zohe(s,(2,5)) == Measure(5,20)
    True
    >>> maximum_zohe(s,(-1,1)) == Measure(1,10)
    True
    >>> maximum_zohe(s,(1,6)) == Measure(6,float("inf"))
    True
    """
    t0,tf = i
    sp = s.interval_temporal(t0,tf,Zohe)
    return maximum(sp,i)
    
def last_zohe(s,i):
    """
    Agregador last ZOHE

    >>> m1 = Measure(1,10); m2 = Measure(2,40); m3 = Measure(5,20)
    >>> s = TimeSeries([m1,m2,m3])
    >>> last_zohe(s,(1,5)) == Measure(5,20)
    True
    >>> last_zohe(s,(2,5)) == Measure(5,20)
    True
    >>> last_zohe(s,(-1,1)) == Measure(1,10)
    True
    >>> last_zohe(s,(-1,1.5)) == Measure(1.5,40)
    True
    >>> last_zohe(s,(1,6)) == Measure(6,float("inf"))
    True
    """
    t0,tf = i
    sp = s.interval_temporal(tf,tf,Zohe)
    return sp.pop()







def zohe_u(fzohe,s,i):
    """
    Agregador que tracta dades desconegudes com a zero i després
    aplica l'agregador `fzohe`.

    >>> m1 = Measure(1,10); m2 = Measure(2,float("inf")); m3 = Measure(5,40)
    >>> s = TimeSeries([m1,m2,m3])
    >>> zohe_u(area_zohe, s,(1,5)) == Measure(5,120)
    True
    >>> zohe_u(area_zohe,s,(0,5)) == Measure(5,130)
    True
    >>> zohe_u(area_zohe,s,(-1,5)) == Measure(5,140)
    True
    >>> zohe_u(area_zohe,s,(0.5,3.5)) == Measure(3.5,65)
    True
    >>> zohe_u(area_zohe,s,(0,6)) == Measure(6,130)
    True
    >>> zohe_u(area_zohe,s,(0,1)) == Measure(1,10)
    True
    >>> zohe_u(area_zohe,s,(0,1.5)) == Measure(1.5,10)
    True
    """
    t0,tf = i

    sp = s.interval_temporal(t0,tf,Zohe)
    sp = sp.map(lambda m: Measure(m.t, 0 if math.isinf(m.v) else m.v))

    return fzohe(sp,i)

