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
