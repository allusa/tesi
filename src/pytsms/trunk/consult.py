"""
Useful consult operators
"""


from pytsms import Measure, TimeSeries




def multiresolution(s,schema):
    """
    >>> def _max(s,i): sp=s[i[0]:i[1]]; return Measure(i[1], None if len(sp)==0 else max(sp.projection('v')))
    >>> s = TimeSeries([Measure(5,5),Measure(11,1),Measure(12,2),Measure(16,1),Measure(21,1),Measure(26,1)])
    >>> schema = TimeSeries([Measure(5,(10,_max,4)),Measure(10,(0,_max,3))])
    >>> multiresolution(s,schema) == TimeSeries([Measure(15,2),Measure(20,1),Measure(25,1),Measure(10,5)])
    True
    """
    def fr(si,mi):
        deltac = mi.t
        tauc,fc,kc = mi.v
        return si.concatenate(dmap(s,deltac,tauc,fc,kc))
    return schema.orderfold(fr,min,TimeSeries())


def dmap(sb,delta,tau,f,k):
    """
    >>> def _max(s,i): sp=s[i[0]:i[1]]; return Measure(i[1], None if len(sp)==0 else  max(sp.projection('v')))
    >>> s = TimeSeries([Measure(11,1),Measure(12,2),Measure(16,1),Measure(21,1),Measure(26,1)])
    >>> dmap(s,5,10,_max,4) == TimeSeries([Measure(15,2),Measure(20,1),Measure(25,1)])
    True
    >>> dmap(s,5,10,_max,5) == TimeSeries([Measure(15,2),Measure(20,1),Measure(25,1)])
    True
    >>> dmap(s,5,0,_max,4) == TimeSeries([Measure(5,None),Measure(10,None),Measure(15,2),Measure(20,1)])
    True
    >>> s2 = TimeSeries([Measure(5,5),Measure(11,1),Measure(12,2),Measure(16,1),Measure(21,1),Measure(26,1)])
    >>> dmap(s2,5,10,_max,4) ==  dmap(s,5,10,_max,4)
    True
    """

    ti = range(tau,tau+(k+1)*delta,delta)
    ti = filter(lambda t: tau <= t <= sb.sup().t, ti)
    si = TimeSeries([Measure(t,None) for t in ti ])

    def fmap(mi):
        i = [si.prev(mi).t,mi.t]
        mp= f(sb,i)
        return mp

    s = si.map(fmap)

    return s.selection(lambda m: m.t > s.inf().t)






def translation(s,delta):
    """
    >>> s1 = TimeSeries([Measure(1,1),Measure(2,2),Measure(3,3)])
    >>> translation(s1,1) == TimeSeries([Measure(2,1),Measure(3,2),Measure(4,3)])
    True
    """
    def transd(m):
        return Measure(m.t+delta,m.v)
    return s.map(transd)


def _onecorrelation(s1,s2):
    """
    >>> s1 = TimeSeries([Measure(1,1),Measure(2,2),Measure(3,3)])
    >>> s2 = TimeSeries([Measure(1,1),Measure(2,2),Measure(3,3)])
    >>> _onecorrelation(s1,s2) == Measure(1,14)
    True
    """
    def v1perv2(m):
        return Measure(m.t,m.v[0]*m.v[1])
    def vsum(mi,m):
        return Measure(min(mi.t,m.t),mi.v+m.v)
    
    sjoin = s1.join(s2)
    sper = sjoin.map(v1perv2)
    ssum = sper.aggregate(vsum)
    return ssum

    
def correlation(s1,s2,step=1):
    """
    >>> s = TimeSeries([Measure(1,1),Measure(2,2),Measure(3,3)])
    >>> correlation(s,s) == TimeSeries([Measure(1,14),Measure(2,8),Measure(3,3)])
    True
    >>> correlation(s,s,2)  == TimeSeries([Measure(1,14),Measure(3,3)])
    True
    """
    res = s1.empty()
    
    tinitial = min(s1).t
    tend = max(s1).t
    for delta in range(0,tend-tinitial+step,step):
        res.add(_onecorrelation(s1,translation(s2,delta)))
    
    return res
