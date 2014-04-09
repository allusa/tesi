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
from pytsms import Measure,TimeSeries      
            

class MRD(MultiresolutionSeries):
    """
    Base de dades multiresolució com una  única sèrie temporal multiresolució
    """
    pass






def MTSMSequivalenceTSMS(s,schema):
    """
    >>> from pytsms.consult import multiresolution
    >>> s = TimeSeries([Measure(5,5),Measure(11,1),Measure(12,2),Measure(16,1),Measure(21,1),Measure(26,1)])
    >>> def _max(s,i): sp=s[i[0]:i[1]]; return Measure(i[1], None if len(sp)==0 else max(sp.projection('v')))
    >>> schema = [(5,4,_max,10),(10,3,_max,0)]
    >>> MTSMSequivalenceTSMS(s,schema)
    True
    """
    from pytsms.consult import multiresolution
    
    schemats = TimeSeries()
    m = MultiresolutionSeries()
    for delta,k,f,tau in schema:
        m.addResolution(delta,k,f,tau)
        schemats.add(Measure(delta,(tau,f,k)))
    
    m.update(s)
    m.consolidateTotal()
    
    return multiresolution(s,schemats) == m.total()
