# -*- encoding: utf-8 -*-

"""
======
pyTSMS
======

:Author: Aleix Llusà Serra
:Contact: aleix (a) dipse.upc.edu
:Version: 0.1
:Date: 	2014-07-15
:Abstract: Implementació en Python d'un SGBD per sèries temporals (SGST). Python implementation for a Time Series DBMS (TSMS).
:Copyright: GPLv3

Python implementation for a time series DBMS. It is the referent
implementation for the data model TSMS described in
http://escriny.epsem.upc.edu/projects/rrb/

Implementació en Python d'un SGBD per sèries temporals
(SGST). És la implementació de referència del model de dades SGST
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

from timeseries import TimeSeries
from measure import Measure
