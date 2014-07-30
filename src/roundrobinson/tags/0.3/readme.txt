=============
RoundRobinson
=============

:Author: Aleix Llusà Serra
:Contact: aleix (a) dipse.upc.edu
:Version: 0.3
:Date: 	2014-07-15
:Abstract: Python implementation for a Multiresolution Time Series DBMS (MTSMS).
:Copyright: GPLv3
:Depends: pytsms0.1

Python implementation for multiresolution time series (MTSMS). It is
the referent implementation for the data model MTSMS described in
http://escriny.epsem.upc.edu/projects/rrb/


Quick tutorial
==============

As a library it provides MultiresolutionSeries object, which provides
MTSMS funcionality, and Measure and TimeSeries objects from Pytsms,
which provide TSMS funcionality.

In module aggregators there are some predefined attribute aggregate functions, however users can define on their own as they are only Python Function objects:

>>> def myagg(s,i):
...     t0,tf = i
...     etc.



Importing the required objects

>>> from roundrobinson import TimeSeries, Measure as m
>>> from roundrobinson import MultiresolutionSeries
>>> from roundrobinson.aggregators import maximum_zohe

Defining three measures:
>>> m1 = m(1,3); m2 = m(2,1); m3 = m(4,5)

Defining the multiresolution time series
>>> M = MultiresolutionSeries()
Defining the multiresolution schema
>>> M.addResolution(delta=2,k=3,f=maximum_zohe,tau=0)

Adding first measure
>>> M.add(m1)
M is not yet consolidable as t < delta
>>> M.consolidable()
False

Adding second measure
>>> M.add(m2)
M is consolidable as t = delta
>>> M.consolidable()
True
Consolidating
>>> M.consolidate()
Query the time series in consolidated disc
>>> M.seriedisc(2,maximum_zohe)
TimeSeries([m(2,3)])

Adding third measure
>>> M.add(m3)
M is consolidable as t = 2*delta
>>> M.consolidable()
True
Consolidating
>>> M.consolidate()
Query the time series in consolidated disc
>>> M.seriedisc(2,maximum_zohe)
TimeSeries([m(2,3),m(4,5)])

Acknowledgements
================

Amb el suport de la Universitat Politècnica de Catalunya (UPC).

Amb l'agraïment als directors de tesi: Teresa Escobet Canal i Sebastià
Vila Marta.


License
=======

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
