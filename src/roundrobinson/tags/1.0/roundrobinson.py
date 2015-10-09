# -*- encoding: utf-8 -*-

"""
=============
RoundRobinson
=============

:Author: Aleix Llusà Serra
:Contact: aleix (a) dipse.upc.edu
:Version: 0.4-dev
:Date: 	2014-07-15
:Abstract: Implementació en Python d'un SGBD per sèries temporals multiresolució (SGSTM). Python implementation for a Multiresolution Time Series DBMS (MTSMS).
:Copyright: GPLv3
:Depends: pytsms0.2-dev

Python implementation for multiresolution time series (MTSMS). It is
the referent implementation for the data model MTSMS described in
http://escriny.epsem.upc.edu/projects/rrb/

Implementació en Python d'un SGBD per sèries temporals multiresolució
(SGSTM). És la implementació de referència del model de dades SGSTM
descrit a http://escriny.epsem.upc.edu/projects/rrb/

Amb el suport de la Universitat Politècnica de Catalunya (UPC).


Copyright (C) 2012-2014 Aleix Llusà Serra.
 
This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this document. If not, see <http://www.gnu.org/licenses/>.

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
