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
from opset import TimeSeriesSetOp
from opseq import TimeSeriesSeqOp
from opfunc import TimeSeriesFuncOp




class TimeSeries(TimeSeriesSetOp,TimeSeriesSeqOp,TimeSeriesFuncOp,TimeSeriesStructure):
    """
    L'ordre de l'herència és important, `TimeSeriesStructure` ha d'anar
    en darrer lloc per tal que les seves operacions siguin
    redefinides.


    Binary arithmetic operations:
    
    * union for sets, symbol `|` (or), method `union`

    """
    pass




def _s1test():
    """
    Retorna una sèrie temporal de prova
    """
    m1 = Measure(1,10)
    m2 = Measure(2,10)
    m3 = Measure(5,40)

    s = SerieTemporal() 
    s.add(m1)
    s.add(m2)
    s.add(m3)

    return s






# class TimeSeriesTemporal(TimeSeries):
#     """
#     Sèrie Temporal per a operacions temporals

#     >>> import opset
#     >>> s1 = TimeSeriesTemporal([Measure(1,2),Measure(2,1)])
#     >>> s2 = TimeSeriesTemporal([Measure(3,2),Measure(1,2),Measure(2,2)])
#     >>> print s1 | s2
#     >>> s1 | s2 == opset.union_temporal(s1,s2)
#     True
#     >>> s2 | s1 == opset.union_temporal(s2,s1)
#     True
#     """


#     def __in__(self,m):
#         """
#         Pertinença temporal exclusiva, només certa si m pertany
#         temporalment a s i no pertany a s. Equivalent a ta.
#         """
#         if TimeSeries.__in__(self,m):
#             for ms in self:
#                 if ms.eqnt(m):
#                     return False
#             return True
#         return False













class SerieTemporal(set):
    def __init__(self):
        raise DeprecationWarning("Useu TimeSeries")



    def __repr__(self):
        """
        Sobrecàrrega del mètode representació per tal que sempre es
        representi ordenat.
        """
        return 'SerieTemporal({0})'.format( repr(sorted(self)) )



    def esRegular(self):
        """
        Predicat que és cert ssi la sèrie temporal és regular

        """
        """
        >>> s = _s1test()
        >>> s.esRegular()
        False
        >>> s2 = SerieTemporal()
        >>> s2.add(Measure(10,3));s2.add(Measure(10,6));s2.add(Measure(25,9));s2.add(Measure(10,12))
        >>> s2.esRegular()
        True
        """
        r = min(self)
        s = self[r.t:] #S(r,infinit)

        prevdelta = None

        for m in s:
            delta = m.t - self.ant(m).t
            if not prevdelta:
                prevdelta = delta
            elif delta == prevdelta:
                prevdelta = delta
            else:
                return False

        return True


