# -*- encoding: utf-8 -*-

"""
=============
RoundRobinson
=============

:Author: Aleix Llusà Serra
:Contact: aleix (a) dipse.upc.edu
:Version: 0.3-dev
:Date: 	2014-01-08
:Abstract: Implementació en Python d'un SGBD per sèries temporals multiresolució (SGSTM). Python implementation for a Multiresolution Time Series DBMS (MTSMS).
:Copyright: GPLv3
:Depends: pytsms0.1-dev

Implementació en Python d'un SGBD per sèries temporals multiresolució
(SGSTM). És la implementació de referència del model de dades SGSTM
descrit a http://escriny.epsem.upc.edu/projects/rrb/

Amb el suport de la Universitat Politècnica de Catalunya (UPC).
"""

from multiresolution import MultiresolutionSeries                
            
class MRD(MultiresolutionSeries):
    """
    Base de dades multiresolució com una  única sèrie temporal multiresolució
    """
    pass






def MTSMSequivalenceTSMS():
    """
    >>> from pytsms import Measure,TimeSeries
    >>> from pytsms.consult import multiresolution
    >>> s = TimeSeries([Measure(5,5),Measure(11,1),Measure(12,2),Measure(16,1),Measure(21,1),Measure(26,1)])
    >>> def _max(s,i): sp=s[i[0]:i[1]]; return Measure(i[1], None if len(sp)==0 else max(sp.projection('v')))
    >>>
    >>> m = MultiresolutionSeries()
    >>> m.addResolution(5,4,_max,10)
    >>> m.addResolution(10,3,_max,0)
    >>> m.update(s)
    >>> m.consolidateTotal()
    >>>
    >>> schema = TimeSeries([Measure(5,(10,_max,4)),Measure(10,(0,_max,3))])
    >>>
    >>> multiresolution(s,schema) == m.total()
    True
    """
    pass



