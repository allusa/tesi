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

from serietemporal import Mesura,SerieTemporal

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

    
def area(s,i):
    """
    Interpolador àrea

    >>> m1 = Mesura(10,1)
    >>> m2 = Mesura(10,2)
    >>> m3 = Mesura(40,5)
    >>> s = SerieTemporal()
    >>> s.add(m1); s.add(m2); s.add(m3)
    >>>
    >>> area(s,(0,5))
    m(28.0,5)
    >>> area(s,(-1,5))
    m(25.0,5)
    >>> area(s,(0,4))
    m(25.0,4)
    >>> area(s,(0.5,3.5))
    m(25.0,3.5)
    >>> area(s,(0,6))
    m(inf,6)
    >>> #area(s,(0,1))
    >>> #area(s,(-1,0))
    """
    t0 = i[0]
    tf = i[1]

    o = min( s[t0:tf] )
    os = SerieTemporal(); os.add(o)
    sp = s[t0:tf] - os
    n = s.seg( max(sp) )

    
    if math.isinf(n.v) and (tf-s.ant(n).t) == 0:
        # s'aplica la definició 0xinf=0, com es fa típicament a la teoria de mesura
        v = (o.t-t0)*o.v  # + 0*float("inf")
    else:
        v = (o.t-t0)*o.v + (tf-s.ant(n).t)*n.v

    for m in sp:
        v += (m.t-s.ant(m).t)*m.v

    v /= float(tf-t0)
    return Mesura(v,tf)    
    
