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
    >>> s0 = TimeSeries([])
    >>> mean(s0,(0,5)) == Measure(5,float("inf"))
    True
    """
    mtype = s.mtype()
    t0,tf = i
    sp = s.interval_open_left(t0,tf)
    v = sp.aggregate(lambda mi,m: Measure(mi.t+1, mi.v+m.v), Measure(0,0))
    if v.t == 0:
        return mtype(tf,float("inf"))
    return mtype(tf, v.v / float(v.t) )


def maximum(s,i):
    """
    Agregador màxim discret amb T(m')=tf

    >>> m1 = Measure(1,10); m2 = Measure(2,40); m3 = Measure(5,20)
    >>> s = TimeSeries([m1,m2,m3])
    >>> maximum(s,(0,5)) == Measure(5,40)
    True
    >>> maximum(s,(0,6)) == Measure(6,40)
    True
    >>> s0 = TimeSeries([])
    >>> maximum(s0,(0,5)) == Measure(5,float("inf"))
    True
    """
    mtype = s.mtype()
    t0,tf = i
    sp = s.interval_open_left(t0,tf)

    if len(sp) == 0:
        return mtype(tf,float("inf"))

    v = max(sp.projection(['v']))
    return mtype(tf,v)

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
    mtype = s.mtype()
    t0,tf = i
    sp = s.interval_open_left(t0,tf)
    v = max(sp).v
    return mtype(tf,v)


    
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
    >>> area_zohe(s,(0,1)) == Measure(1,10)
    True
    >>> area_zohe(s,(-1,0)) == Measure(0,10)
    True
    >>> area_zohe(s,(0,6)) == Measure(6,None) #no es pot calcular
    True
    >>> from pytsms.measure import MeasureInf
    >>> m1 = MeasureInf(1,10); m2 = MeasureInf(2,10); m3 = MeasureInf(5,40)
    >>> s2 = TimeSeries([m1,m2,m3])
    >>> area_zohe(s2,(0,6)) == MeasureInf(6)
    True
    """
    t0,tf = i

    sp = s.interval_temporal(t0,tf,Zohe)
    if sp.sup().v is None:
        #error, aquesta area no es pot calcular
        return s.mtype()(tf,None)  

    o = min(sp)
    #spp = sp - TimeSeries([o])
    spp = sp[o.t::'l']

    vp = (o.t - t0)*o.v
    #aquesta operacio es molt cara en rendiment:
    vp += reduce(lambda mi,m: mi+(m.t-sp.prev(m).t)*m.v,spp,0)
    #vpp = spp.aggregate(lambda mi,m: Measure(mi.t,mi.v+(m.t-sp.prev(m).t)*m.v), Measure(0,0))
    #vp = vpp.v + vp


    return s.mtype()(tf,vp)  


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
    >>> mean_zohe(s,(0,1)) == Measure(1,10)
    True
    >>> mean_zohe(s,(0,6)) == Measure(6,None)#no es pot calcular
    True
    >>> from pytsms.measure import MeasureInf
    >>> m1 = MeasureInf(1,10); m2 = MeasureInf(2,10); m3 = MeasureInf(5,40)
    >>> s2 = TimeSeries([m1,m2,m3])
    >>> mean_zohe(s2,(0,6)) == MeasureInf(6)
    True
    """
    t0,tf = i
    area = area_zohe(s,i).v
    if area is None:
        return  s.mtype()(tf,None)
    v = area/(tf-t0)
    return  s.mtype()(tf,v)


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
    >>> maximum_zohe(s,(1,6)) == Measure(6,40)
    True
    >>> from pytsms.measure import MeasureInf
    >>> m1 = MeasureInf(1,10); m2 = MeasureInf(2,40); m3 = MeasureInf(5,20)
    >>> s2 = TimeSeries([m1,m2,m3])
    >>> maximum_zohe(s2,(1,6)) == MeasureInf(6)
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
    >>> last_zohe(s,(1,6)) == Measure(6,None)
    True
    """
    t0,tf = i
    sp = s.interval_temporal(tf,tf,Zohe)
    return sp.pop()







def zohe_u(fzohe,s,i):
    """
    Agregador que tracta dades desconegudes com a zero i després
    aplica l'agregador `fzohe`.

    >>> m1 = Measure(1,10); m2 = Measure(2); m3 = Measure(5,40)
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
    sp = sp.map(lambda m: Measure(m.t, 0 if m.isvalueundefined() else m.v))

    return fzohe(sp,i)

