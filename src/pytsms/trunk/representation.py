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



class Representation(object):
    """
    Representació d'una sèrie temporal. Objecte abstracte amb els
    mètodes :py:meth:`Representation.interval_temporal` i
    :py:meth:`Representation.representation` delegats.

    :param s: Sèrie temporal associada a la representació
    :type s: :py:class:`timeseries.TimeSeries`

    """
    
    def __init__(self,s):
        """
        Constructor de la representació amb una sèrie temporal associada
        """
        self._ts = s
    
    def get_ts(self):
        """
        Retorna la sèrie temporal associada
        """
        return self._ts

    def interval_temporal(self,l,g):
        """
        Operador d'interval temporal. Sèrie temporal resultant de
        l'interval temporal sobre la seqüència entre dos temps `l` i `g`.
        El càlcul de l'interval temporal el realitza la representació `rpr`.

        :param l: Instant de temps menor
        :type l: :data:`timeseries.Time`
        :param g:  Instant de temps major
        :type g: :data:`timeseries.Time`
        :returns: `s[l,g]ᵗ`
        :rtype: :class:`timeseries.TimeSeries`
        :raises NotImplementedError: Abstract method, should be delegated
        """
        raise NotImplementedError("Abstract object, method should be delegated")

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
        graf = self.get_ts().graf(l,g,step)
        x,y = zip(*graf)

        pyplot.plot(x,y,'o-')
        pyplot.show()






"""
Some representations
--------------------
"""




class DiscretePure(Representation):
    """
    Representació discreta pura per a les sèries temporals
    """
    pass



class Zohe(Representation):
    """
    Representació ZOHE de Sèrie Temporal.

    >>> from timeseries import TimeSeries
    >>> s = TimeSeries([Measure(5,3),Measure(1,1),Measure(2,2)])
    >>> s.set_representation(Zohe)
    >>> s(2) == s.representation(2)
    True
    >>> s(4) == s.representation(4)
    True
    >>> s.graf(1,4,1)
    [(1, 1), (2, 2), (3, 3)]
    >>> s(2) == s.interval_temporal(2,2).pop().v
    True
    """

    def interval_temporal(self,l,g):
        """
        Operador d'interval temporal ZOHE. 

        :param l: Instant de temps menor
        :type l: :data:`timeseries.Time`
        :param g: Instant de temps major
        :type g: :data:`timeseries.Time`
        :returns: `s[l,g]ᵗZOHE`
        :rtype: :class:`timeseries.TimeSeries`

        >>> from timeseries import TimeSeries
        >>> s = TimeSeries([Measure(5,3),Measure(1,1),Measure(2,2)])
        >>> s.set_representation(Zohe)
        >>> s.interval_temporal(1,4) == TimeSeries([Measure(4,3),Measure(2,2)])
        True
        >>> s.interval_temporal(-5,0) == TimeSeries([Measure(0,1)])
        True
        >>> s.interval_temporal(6,10) == TimeSeries([Measure(10,float("inf"))])
        True
        """       
        s = self.get_ts()
        r = s.interval_open_left(l,g)
        v = s[g::'c'].inf().v
        m = Measure(g,v)
        r.add(m)
        return r


    def representation(self,t):
        """
        Operador de representació ZOHE. Valor resultant d'evaluar la sèrie temporal en l'instant de temps `t` amb representació ZOHE.

        :param t: Instant de temps
        :type t: :data:`timeseries.Time`
        :returns: `s(t)ZOHE`
        :rtype: :data:`timeseries.Value`

        >>> from timeseries import TimeSeries
        >>> s = TimeSeries([Measure(5,3),Measure(1,1),Measure(2,2)])
        >>> s.set_representation(Zohe)
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
        s = self.get_ts()
        if len(s) == 0:
            return 0
        if t > s.sup().t:
            return 0
        
        return s[t::'c'].inf().v


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

        >>> from timeseries import TimeSeries
        >>> s = TimeSeries([Measure(5,3),Measure(1,1),Measure(2,2)])
        >>> s.set_representation(Zohe)
        >>> #s.get_representation().plot()
        """
        s = self.get_ts()
        x = [] #x = [float("-inf")]
        y = [] #y = [s.inf().v]
        for m in sorted(s):
            x.append(m.t)
            y.append(m.v)

        #x.append(float("inf"))
        #y.append(0)

        
        pyplot.plot(x,y,'o-',drawstyle='steps-pre')
        pyplot.show()
