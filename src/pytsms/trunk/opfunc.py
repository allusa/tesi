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
from structure import TimeSeriesStructure



class TimeSeriesFuncOp(TimeSeriesStructure):
    """
    Operadors de funció de Sèrie Temporal
    """
    

    def interval_temporal(self,l,g):
        """
        Operador d'interval temporal. Sèrie temporal resultant de
        l'interval temporal sobre la seqüència entre dos temps `l` i `g`.

        Mètode abstracte, ha de ser delegat.

        :param l: Instant de temps menor
        :type l: :data:`timeseries.Time`
        :param g:  Instant de temps major
        :type g: :data:`timeseries.Time`
        :returns: `s[l,g]ᵗ`
        :rtype: :class:`timeseries.TimeSeries`
        :raises NotImplementedError: Abstract method, should be delegated
        """
        raise NotImplementedError("Abstract object, method should be delegated")


   def selection_temporal(self,tt):
        """
        Operador de selecció temporal. Sèrie temporal resultant de
        seleccionar sobre el conjunt d'instants de temps `tt`.


        :param tt: Conjunt de temps
        :type tt: Iterable of :data:`timeseries.Time`
        :returns: `s{tt}ᵗ`
        :rtype: :class:`timeseries.TimeSeries`
        """
        pass
