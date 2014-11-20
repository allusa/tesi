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

from representation import Representation


class FuncOpMixin():
    """
    Operadors de funció de Sèrie Temporal
   
    * s(t)

    """

    _rpr = None


    def set_rpr(self,rpr):
        """
        Permet definir una representació per defecte de la sèrie
        temporal. S'aplicarà per defecte a tots els operadors de
        funció temporal.

        :param rpr: Una representació per a la sèrie temporal
        :type rpr: :class:`representation.Representation`
        """        
        self._rpr = rpr


    def get_rpr(self):
        """
        Permet obtenir la representació per defecte de la sèrie
        temporal.

        :return: El tipus de representació per a la sèrie temporal
        :rtype: :class:`representation.Representation` or None
        """        
        try:
            return self._rpr
        except AttributeError:
            return None



    def __call__(self,t):
        """
        Crida en funcions

        * s(t)
        """
        return self.representation(t)


    def rpr(self,rpr=None):
        """
        Returns rpr inited with self time series. If rpr is none uses
        the default representation.

        :return: La representació per a la sèrie temporal
        :rtype: :class:`representation.Representation`
        """
        if rpr is None:
            rpr = self.get_rpr()
            if rpr is None:
                return Representation(self)
        return rpr(self)


    def representation(self,t,rpr=None):
        """
        Operador de representació. Valor resultant d'evaluar la sèrie temporal en l'instant de temps `t`.

        :param t: Instant de temps
        :type t: :data:`timeseries.Time`
        :returns: `s(t)ᵗ`
        :rtype: :data:`timeseries.Value`
        """
        return self.rpr(rpr).representation(t)


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
        return [ (t,self.representation(t)) for t in range(l,g,step) ]


    def plot(self,rpr=None):
        self.rpr(rpr).plot()


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
        >>> s.set_rpr(Zohe)
        >>> s.interval_temporal(1,4) == TimeSeries([Measure(4,3),Measure(2,2)])
        True
        >>> s.interval_temporal(-5,0) == TimeSeries([Measure(0,1)])
        True
        >>> s.interval_temporal(6,10) == TimeSeries([Measure(10,None)])
        True
        """
        return self.rpr(rpr).interval_temporal(l,g)
        


    def selection_temporal(self,tt,rpr=None):
        """
        Operador de selecció temporal. Sèrie temporal resultant de
        seleccionar sobre el conjunt d'instants de temps `tt`.


        :param tt: Conjunt de temps
        :type tt: Iterable of :data:`timeseries.Time`
        :param rpr: Representació de la sèrie temporal,
        :type rpr: :class:`representation.Representation`
        :returns: `s{tt}ᵗ`, selecció temporal de s en tt
        :rtype: :class:`timeseries.TimeSeries`

        >>> from timeseries import TimeSeries
        >>> from representation import Zohe
        >>> s = TimeSeries([Measure(8,3),Measure(1,1),Measure(2,2)])
        >>> tt = range(1,8,2)
        >>> s.selection_temporal(tt,Zohe) == TimeSeries([Measure(5,3),Measure(1,1),Measure(3,3),Measure(7,3)])
        True
        >>> s.set_rpr(Zohe)
        >>> s.selection_temporal(tt) == TimeSeries([Measure(5,3),Measure(1,1),Measure(3,3),Measure(7,3)])
        True
        >>> s.get_rpr() == Zohe
        True
        """
        s = self.empty()
        
        copiarpr = s._rpr #ERROR en el COPY

        for t in tt:
            s = s.union(self.interval_temporal(t,t,rpr))
        
        s._rpr = copiarpr #ERROR en el COPY
        return s



    def concatenate_temporal(self,other,rpr=None):
        """
        Operador de concatenació temporal. Sèrie temporal resultant de
        concatenar temporalment amb la sèrie temporal `other`.


        :param other: 
        :type other: :class:`timeseries.TimeSeries`
        :param rpr: Representació de la sèrie temporal,
        :type rpr: :class:`representation.Representation`
        :returns: `s1 ||ᵗ s2`, concatenació temporal de s1 i s2
        :rtype: :class:`timeseries.TimeSeries`

        >>> from timeseries import TimeSeries
        >>> from representation import Zohe
        >>> s1 = TimeSeries([Measure(5,1),Measure(1,1),Measure(2,1)])
        >>> s1.set_rpr(Zohe)
        >>> s2 = TimeSeries([Measure(4,2),Measure(0,2),Measure(1,2),Measure(6,2)])
        >>> s2.set_rpr(Zohe)
        >>> s1.concatenate_temporal(s2) == TimeSeries([Measure(5,1),Measure(1,2),Measure(2,1),Measure(0,2),Measure(6,2)])
        True
        >>> s2.concatenate_temporal(s1) == s2
        True
        """
        t1 = self.inf().t
        t2 = self.sup().t

        if rpr is None:
            rpr = self.get_rpr()

        s1 = self.interval_temporal(t1,t2,rpr)
        s2a = other.interval_temporal(None,t1,rpr)
        s2b = other.interval_temporal(t2,None,rpr)
        return s1.union(s2a).union(s2b)



    def join_temporal(self,other,rpr=None):
        """
        Operador de junció temporal. Sèrie temporal resultant
        d'ajuntar temporalment amb la sèrie temporal `other`.


        :param other: 
        :type other: :class:`timeseries.TimeSeries`
        :param rpr: Representació de la sèrie temporal,
        :type rpr: :class:`representation.Representation`
        :returns: `s1 joinᵗ s2`, junció temporal de s1 i s2
        :rtype: :class:`timeseries.TimeSeries`

        >>> from timeseries import TimeSeries
        >>> from representation import Zohe
        >>> s1 = TimeSeries([Measure(5,1),Measure(1,1),Measure(2,1)])
        >>> s1.set_rpr(Zohe)
        >>> s2 = TimeSeries([Measure(4,2),Measure(0,2),Measure(1,2),Measure(6,2)])
        >>> s2.set_rpr(Zohe)
        >>> s1.join_temporal(s2) == TimeSeries([Measure(0,(1,2)),Measure(1,(1,2)),Measure(2,(1,2)),Measure(4,(1,2)),Measure(5,(1,2)),Measure(6,(None,2))])
        True
        >>> ##s2.join_temporal(s1) == swapv1v2(s1.join_temporal(s2))
        """
        tp = self.t().union(other.t())
        s1tp = self.selection_temporal(tp,rpr)
        s2tp = other.selection_temporal(tp,rpr)
    
        return s1tp.join(s2tp)


    def semijoin_temporal(self,other,rpr=None):
        """
        Operador de semijunció temporal. Sèrie temporal resultant
        de semiajuntar temporalment amb la sèrie temporal `other`.


        :param other: 
        :type other: :class:`timeseries.TimeSeries`
        :param rpr: Representació de la sèrie temporal,
        :type rpr: :class:`representation.Representation`
        :returns: `s1 semijoinᵗ s2`, semijunció temporal de s1 i s2
        :rtype: :class:`timeseries.TimeSeries`

        >>> from timeseries import TimeSeries
        >>> from representation import Zohe
        >>> s1 = TimeSeries([Measure(5,1),Measure(1,1),Measure(2,1)])
        >>> s1.set_rpr(Zohe)
        >>> s2 = TimeSeries([Measure(4,2),Measure(0,2),Measure(1,2),Measure(6,2)])
        >>> s2.set_rpr(Zohe)
        >>> s1.semijoin_temporal(s2) == TimeSeries([Measure(1,(1,2)),Measure(2,(1,2)),Measure(5,(1,2))])
        True
        >>> s2.semijoin_temporal(s1) == TimeSeries([Measure(0,(2,1)),Measure(1,(2,1)),Measure(4,(2,1)),Measure(6,(2,None))])
        True
        """
        tp = self.t()
        s2 = other.selection_temporal(tp,rpr)
        return self.join_temporal(s2,rpr)



