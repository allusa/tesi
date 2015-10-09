======
pyTSMS
======

:Author: Aleix Llusà Serra
:Contact: aleix (a) dipse.upc.edu
:Version: 1.0 (tesi)
:Date: 	2015-10-09
:Abstract: Python implementation for a Time Series DBMS (TSMS).
:Copyright: GPLv3
:Depends: python2.7


Python implementation for a time series DBMS. It is the referent
implementation for the data model TSMS described in
http://escriny.epsem.upc.edu/projects/rrb/



Installation
============

This is implemented as a Python library. There is not an official
release yet.  It can be installed as a Python library, rename this directory to `pytsms` and choose:

* To only test use it locally with `python`.  

* To use as a locally installed library, copy it to `/usr/local/lib/python2.7/dist-packages/pytsms/`.  

* Create a virtualenv.


It has only been tested with python2.7.



Quick tutorial
==============


Importing the required objects

>>> from pytsms import TimeSeries, Measure as m




Acknowledgements
================

Amb el suport de la Universitat Politècnica de Catalunya (UPC).

Amb l'agraïment als directors de tesi: Teresa Escobet Canal i Sebastià
Vila Marta.


License
=======

Copyright (C) 2012-2015 Aleix Llusà Serra.
 
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
