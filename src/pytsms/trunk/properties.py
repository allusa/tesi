# -*- encoding: utf-8 -*-

"""
==================================
Propietats de les sèries temporals
==================================

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació de les propietats de les sèries temporals.
"""

from measure import Measure


class RegularProperties(object):
    """
    Propietats de regularitat d'una sèrie temporal

    :param s: sèrie temporal
    :type s: :class:`timeseries.TimeSeries`

    """

    def __init__(self,s):
        """
        Constructor de les propietats regulars relacionades amb una sèrie temporal
        """
        self._s = s



    def isRegular(self,ti=None):
        """
        Predicat que és cert ssi la sèrie temporal és regular

        :param ti: (Opcional) Instant de temps d'inici
        :type ti: :data:`timeseries.Time`
        :return: Cert si i només si `s` és regular
        :rtype: bool

        >>> from timeseries import TimeSeries
        >>> s = TimeSeries([Measure(1,1),Measure(2,1),Measure(3,1)])
        >>> r = RegularProperties(s)
        >>> r.isRegular()
        True
        >>> r.isRegular(1)
        True
        >>> r.isRegular(2)
        False
        >>> s2 = TimeSeries([Measure(1,1),Measure(2,1),Measure(4,1)])
        >>> r2 = RegularProperties(s2)
        >>> r2.isRegular()
        False
        """
        mmin = min(self._s)
        tmin = mmin.t
        if ti is not None and tmin != ti:
            return False

        s = self._s.interval_open(tmin,float("inf")) #S(r,infinit)

        def tdelta(si,m):
            td = m.t - self._s.prev(m).t
            si.add(Measure(m.t,td))
            return si

        sdelta = s.fold(tdelta,self._s.empty())
        
        return len(sdelta.projection(['v'])) == 1



    def regularise(self,delta,ti=None,te=None,rpr=None,):
        """
        Retorna una sèrie temporal regular en els intants ti+n*delta

        :param delta: Durada de temps del pas 
        :type delta: :data:`timeseries.Time`
        :param ti: (Opcional) Instant de temps d'inici o min(s)
        :type ti: :data:`timeseries.Time`
        :param te: (Opcional) Instant de temps final o max(s)
        :type te: :data:`timeseries.Time`
        :param rpr: (Opcional) Representació de la sèrie temporal
        :type rpr: :class:`representation.Representation`
        :return: Una sèrie temporal regularitzada segons la representació
        :rtype: :class:`timeseries.TimeSeries`

        >>> from timeseries import TimeSeries
        >>> from representation import Zohe
        >>> s = TimeSeries([Measure(1,1),Measure(2,1),Measure(5,1)])
        >>> r = RegularProperties(s)
        >>> r.regularise(1,rpr=Zohe) == TimeSeries([Measure(1,1),Measure(2,1),Measure(3,1),Measure(4,1),Measure(5,1)])
        True
        >>> r.regularise(2,0,8,Zohe) == TimeSeries([Measure(0,1),Measure(2,1),Measure(4,1),Measure(6,float("inf"))])
        True
        >>> s.set_rpr(Zohe)
        >>> r.regularise(1) == r.regularise(1,rpr=Zohe)
        True
        """
        if ti is None:
            ti = self._s.inf().t
        if te is None:
            te = self._s.sup().t + delta

        tt = range(ti,te,delta)

        return self._s.selection_temporal(tt,rpr)

