# -*- encoding: utf-8 -*-

"""
==========================================
Operadors de funció per a sèries temporals
==========================================

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació dels operadors de funció de Sèrie Temporal.
"""

from measure import Measure


class TimeSeriesFuncOp(object):
    """
    Operadors de funció de Sèrie Temporal
   
    * s(t)

    """

    def __call__(self,t):
        """
        Crida en funcions

        * s(t)
        """
        return self.representation(t)


    def set_representation(self,rpr):
        """
        Permet definir una representació per defecte de la sèrie
        temporal. S'aplicarà per defecte a tots els operadors de
        funció temporal.

        :param rpr: Una representació per a la sèrie temporal
        :type rpr: :class:`representation.Representation`
        """        
        self._representation = rpr(self)


    def get_representation(self):
        """
        Permet obtenir la representació per defecte de la sèrie
        temporal.

        :return: La representació per a la sèrie temporal
        :rtype: :class:`representation.Representation`
        """        
        return self._representation


    def _rpr(self,rpr):
        """
        Returns rpr inited with self time series. If rpr is none uses
        the default representation.
        """
        if rpr is None:
            return self.get_representation()
        return rpr(self)


    def representation(self,t,rpr=None):
        """
        Operador de representació. Valor resultant d'evaluar la sèrie temporal en l'instant de temps `t`.

        :param t: Instant de temps
        :type t: :data:`timeseries.Time`
        :returns: `s(t)ᵗ`
        :rtype: :data:`timeseries.Value`
        """
        return self._rpr(rpr).representation(t)


    def graf(self,l,g,step):
        """
        Operador de graf. Llista de parelles (temps,valor) resultants d'evaluar la sèrie temporal en els instant de temps l+n*step < g, n=0,1,2...

        :param l: Instant de temps menor
        :type l: :data:`timeseries.Time`
        :param g: Instant de temps major
        :type g: :data:`timeseries.Time`
        :param step: Duració de temps
        :type step: :data:`timeseries.Time`
        :returns: `graf s(t)ᵗ`
        :rtype: list of tuples
        """
        r = []
        for t in range(l,g,step):
            r.append((t,self.representation(t)))
        return r


    def interval_temporal(self,l,g,rpr=None):
        """
        Operador d'interval temporal. Sèrie temporal resultant de
        l'interval temporal sobre la seqüència entre dos temps `l` i `g`.
        El càlcul de l'interval temporal el realitza la representació `rpr`.

        :param l: Instant de temps menor
        :type l: :data:`timeseries.Time`
        :param g:  Instant de temps major
        :type g: :data:`timeseries.Time`
        :param rpr: Representació de la sèrie temporal,
        :type rpr: :class:`representation.Representation`
        :returns: `s[l,g]ᵗ`
        :rtype: :class:`timeseries.TimeSeries`


        >>> from timeseries import TimeSeries
        >>> from representation import Zohe
        >>> s = TimeSeries([Measure(5,3),Measure(1,1),Measure(2,2)])
        >>> s.set_representation(Zohe)
        >>> s.interval_temporal(1,4) == TimeSeries([Measure(4,3),Measure(2,2)])
        True
        >>> s.interval_temporal(-5,0) == TimeSeries([Measure(0,1)])
        True
        >>> s.interval_temporal(6,10) == TimeSeries([Measure(10,float("inf"))])
        True
        """
        return self._rpr(rpr).interval_temporal(l,g)
        


    def selection_temporal(self,tt,rpr=None):
        """
        Operador de selecció temporal. Sèrie temporal resultant de
        seleccionar sobre el conjunt d'instants de temps `tt`.


        :param tt: Conjunt de temps
        :type tt: Iterable of :data:`timeseries.Time`
        :returns: `s{tt}ᵗ`, selecció temporal de s en tt
        :rtype: :class:`timeseries.TimeSeries`

        >>> from timeseries import TimeSeries
        >>> from representation import Zohe
        >>> s = TimeSeries([Measure(8,3),Measure(1,1),Measure(2,2)])
        >>> tt = range(1,8,2)
        >>> s.selection_temporal(tt,Zohe) == TimeSeries([Measure(5,3),Measure(1,1),Measure(3,3),Measure(7,3)])
        True
        """
        s = type(self)()
        for t in tt:
            s = s.union(self.interval_temporal(t,t,rpr))
        return s




