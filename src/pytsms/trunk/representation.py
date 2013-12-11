# -*- encoding: utf-8 -*-

"""
========================================
Representació i graf de sèries temporals
========================================

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació de la representació i graf de Sèrie Temporal.
"""

from matplotlib import pyplot

from measure import Measure
from structure import TimeSeriesStructure
from opseq import TimeSeriesSeqOp


class TimeSeriesRepresentation(TimeSeriesStructure):
    """
    Representació com a funció de Sèrie Temporal. Objecte abstracte
    amb el mètode :py:meth:`TimeSeriesRepresentation.representation`
    delegat.
    """


    def __call__(self,t):
        """
        Crida en funcions

        * s(t)
        """
        return self.representation(t)



    def representation(self,t):
        """
        Operador de representació. Valor resultant d'evaluar la sèrie temporal en l'instant de temps `t`.

        :param t: Instant de temps
        :type t: :data:`timeseries.Time`
        :returns: `s(t)ᵗ`
        :rtype: :data:`timeseries.Value`
        :raises NotImplementedError: Abstract method, should be delegated
        """
        raise NotImplementedError("Abstract object, method should be delegated")


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

    def plot(self,l,g,step):
        """
        Operador de gràfic genèric. Grafica el graf de la sèrie temporal.

        Es pot sobrecarregar el mètode per tal de dibuixar un gràfic
        més d'acord amb la representació de la sèrie temporal.

        :param l: Instant de temps menor
        :type l: :data:`timeseries.Time`
        :param g: Instant de temps major
        :type g: :data:`timeseries.Time`
        :param step: Duració de temps
        :type step: :data:`timeseries.Time`
        :returns: pyplot
        """
        graf = self.graf(l,g,step)
        x,y = zip(*graf)

        pyplot.plot(x,y,'o-')
        pyplot.show()








class TimeSeriesZohe(TimeSeriesSeqOp,TimeSeriesRepresentation):
    """
    Representació ZOHE de Sèrie Temporal.

    >>> s = TimeSeriesZohe([Measure(5,3),Measure(1,1),Measure(2,2)])
    >>> s(2) == s.representation(2)
    True
    >>> s(4) == s.representation(4)
    True
    >>> s.graf(1,4,1)
    [(1, 1), (2, 2), (3, 3)]
    """
    def representation(self,t):
        """
        Operador de representació ZOHE. Valor resultant d'evaluar la sèrie temporal en l'instant de temps `t` amb representació ZOHE.

        :param t: Instant de temps
        :type t: :data:`timeseries.Time`
        :returns: `s(t)ZOHE`
        :rtype: :data:`timeseries.Value`

        >>> s = TimeSeriesZohe([Measure(5,3),Measure(1,1),Measure(2,2)])
        >>> s.representation(2)
        2
        >>> s.representation(4)
        3
        >>> s.representation(0)
        1
        >>> s.representation(6)
        0
        >>> s.representation(-10)
        1
        """
        if len(self) == 0:
            return 0
        if t > self.sup().t:
            return 0
        
        return self[t::'c'].inf().v


    def plot(self,l=None,g=None,step=None):
        """
        Operador de gràfic ZOHE. Grafica el graf ZOHE de la sèrie temporal.

        :param l: Instant de temps menor
        :type l: :data:`timeseries.Time`
        :param g: Instant de temps major
        :type g: :data:`timeseries.Time`
        :param step: Duració de temps no té sentit en aquest cas
        :type step: :data:`timeseries.Time`
        :returns: pyplot

        >>> s = TimeSeriesZohe([Measure(5,3),Measure(1,1),Measure(2,2)])
        >>> #s.plot()
        """
        x = [] #x = [float("-inf")]
        y = [] #y = [self.inf().v]
        for m in self:
            x.append(m.t)
            y.append(m.v)

        #x.append(float("inf"))
        #y.append(0)

        pyplot.plot(x,y,'o-',drawstyle='steps-pre')
        pyplot.show()
