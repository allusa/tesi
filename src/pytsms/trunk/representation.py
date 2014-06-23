# -*- encoding: utf-8 -*-

"""
========================================
Representació i graf de sèries temporals
========================================

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació de la representació i graf de Sèrie Temporal.
"""

#Hi ha un bug al Matplotlib????
#Per defecte fa 'TkAgg' i no funciona?
import matplotlib
matplotlib.use('GTKAgg')
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
        """
        return self.interval_temporal(t,t).pop().v




    def plot(self):
        """
        Operador de gràfic genèric. 

        Es pot sobrecarregar el mètode per tal de dibuixar un gràfic
        més d'acord amb la representació de la sèrie temporal.

        :returns: pyplot

        >>> from timeseries import TimeSeries
        >>> s = TimeSeries([Measure(5,3),Measure(1,1),Measure(2,2)])
        >>> #s.plot()
        
        """
        graf = [(m.t,m.v) for m in sorted(self.get_ts())] 
        x,y = zip(*graf)

        pyplot.plot(x,y,'o')
        pyplot.show()

    def plot_graf(self,l=None,g=None,step=None):
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

    def _default_plot_format(self):
        
        pyplot.xticks(rotation=15)
        pyplot.grid(True)





"""
Some representations
--------------------
"""




class Delta(Representation):
    """
    Representació delta per a les sèries temporals

    s(t)delta = s(t) if t in s.t() else 0

    >>> from timeseries import TimeSeries
    >>> s = TimeSeries([Measure(5,3),Measure(1,1),Measure(2,2)])
    >>> s.set_rpr(Delta)
    >>> s.representation(1)
    1
    >>> s.representation(4)
    0
    >>> s.representation(6)
    0
    """
    def interval_temporal(self,l,g):
        """
        Operador d'interval temporal ZOHE. 

        :param l: Instant de temps menor
        :type l: :data:`timeseries.Time`
        :param g: Instant de temps major
        :type g: :data:`timeseries.Time`
        :returns: `s[l,g]ᵗdelta`
        :rtype: :class:`timeseries.TimeSeries`

        >>> from timeseries import TimeSeries
        >>> s = TimeSeries([Measure(5,3),Measure(1,1),Measure(2,2)])
        >>> s.set_rpr(Delta)
        >>> s.interval_temporal(1,4) == TimeSeries([Measure(4,0),Measure(2,2),Measure(1,1)])
        True
        >>> s.interval_temporal(-5,0) == TimeSeries([Measure(0,0),Measure(-5,0)])
        True
        >>> s.interval_temporal(6,10) == TimeSeries([Measure(10,0),Measure(6,0)])
        True
        """  
        s = self.get_ts()
        r = s.interval_closed(l,g) 

        ml = s.mtype()(l,0)
        mg = s.mtype()(g,0)
        r.add(ml)
        r.add(mg)
        return r   



class Zohe(Representation):
    """
    Representació ZOHE de Sèrie Temporal.

    >>> from timeseries import TimeSeries
    >>> s = TimeSeries([Measure(5,3),Measure(1,1),Measure(2,2)])
    >>> s.set_rpr(Zohe)
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
        >>> s.set_rpr(Zohe)
        >>> s.interval_temporal(1,4) == TimeSeries([Measure(4,3),Measure(2,2)])
        True
        >>> s.interval_temporal(-5,0) == TimeSeries([Measure(0,1)])
        True
        >>> s.interval_temporal(6,10) == TimeSeries([Measure(10,None)])
        True
        """       
        s = self.get_ts()
        r = s.interval_open_left(l,g)
        v = s[g::'c'].inf().v
        m = s.mtype()(g,v)
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
        >>> s.set_rpr(Zohe)
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


    def plot(self,l=None,g=None,step=None,formatx=None,legend=None):
        """
        Operador de gràfic ZOHE. Grafica el graf ZOHE de la sèrie temporal.

        :param l: Instant de temps menor
        :type l: :data:`timeseries.Time`
        :param g: Instant de temps major
        :type g: :data:`timeseries.Time`
        :param step: Duració de temps no té sentit en aquest cas
        :param formatx: Format de l'eix x
        :type formatx: function
        :type step: :data:`timeseries.Time`
        :returns: pyplot

        >>> from timeseries import TimeSeries
        >>> import datetime
        >>> s = TimeSeries([Measure(5,3),Measure(1,1),Measure(2,2)])
        >>> s.set_rpr(Zohe)
        >>> #s.plot()
        >>>
        >>> s = TimeSeries([Measure(5,[3,4]),Measure(1,[1,2]),Measure(2,[2,3])])
        >>> s.set_rpr(Zohe)
        >>> def timestamp(t): return datetime.datetime.fromtimestamp(t)
        >>> #s.rpr().plot(formatx=timestamp,legend=['primer','segon'])
        """
        s = self.get_ts()
        x = [] #x = [float("-inf")] #punt teoric
        y = [] #y = [s.inf().v]
        for m in sorted(s):
            if formatx is not None:
                t = formatx(m.t)
            else:
                t = m.t
            x.append(t)
            y.append(m.v)

        #darrer punt teoric a (infinit,0)
        #x.append(float("inf"))
        #y.append(0)


        
        self._default_plot_format()

        pyplot.plot(x,y,'o-',drawstyle='steps-pre')

        if legend is not None:
            pyplot.legend(legend)

        pyplot.show()

