"""
Useful consult operators
"""


from pytsms import Measure, TimeSeries


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
