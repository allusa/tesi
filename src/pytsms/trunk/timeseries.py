# -*- encoding: utf-8 -*-

"""
================
Sèries temporals
================

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació de Sèrie Temporal.


.. py:data:: Time

   El temps és un objecte de qualsevol tipus (int, float, datetime,
   etc.) que tingui un ordre total, mètrica i sigui tancat.

.. py:data:: Value

   El valor és un objecte de qualsevol tipus (string, int, float, list).


"""


from measure import Measure
from structure import TimeSeriesStructure
from opmixins import SetOpMixin, SeqOpMixin
from opfunc import FuncOpMixin

from storage import TimeSeriesStorage



class TimeSeries(FuncOpMixin,SeqOpMixin,SetOpMixin,TimeSeriesStructure):
    """
    L'ordre de l'herència és important, `TimeSeriesStructure` ha d'anar
    en darrer lloc per tal que les seves operacions siguin
    redefinides.
    """
    def __repr__(self):
        """
        Sobrecàrrega del mètode representació per tal que sempre es
        representi ordenat.
        """
        return 'TimeSeries({0})'.format( repr(sorted(self)) ) 


    def storage(self):
        """
        Retorna un objecte amb totes les operacions d'emmagatzematge al disc
        """
        return TimeSeriesStorage(self)





class TimeSeriesVisitable(TimeSeries):
    def accept(self, visitor):
        visitor(self)


