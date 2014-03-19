# -*- encoding: utf-8 -*-

"""
==============
RoundRobindoop
==============

:Author: Aleix Llusà Serra
:Contact: aleix (a) dipse.upc.edu
:Version: 0.1-dev
:Date: 	2014-02-27
:Abstract: Implementació en Hadoop i Python d'un SGBD per sèries temporals multiresolució (SGSTM). Hadoop and Python implementation for a Multiresolution Time Series DBMS (MTSMS).
:Copyright: GPLv3
:Depends: pytsms0.1-dev

Implementació en Python d'un SGBD per sèries temporals multiresolució
(SGSTM). És la implementació amb computació paral·lela del model de dades SGSTM
descrit a http://escriny.epsem.upc.edu/projects/rrb/

Amb el suport de la Universitat Politècnica de Catalunya (UPC).
"""

from roundrobinson import MultiresolutionSeries, Measure, TimeSeries

from timeseriesdoop import TsDoopPipe


class MultiDoop(MultiresolutionSeries):
    """
    Especialitació de les sèries multiresolució amb consolidació via rrdoop


    >>>
    >>> def mitjana(s,i):
    ...     sp = s.interval_open_left(i[0],i[1])
    ...     v = sp.aggregate(lambda mi,m: Measure(mi.t+1, mi.v+m.v), Measure(0,0))
    ...     return Measure(i[1], v.v / float(v.t) )
    >>> 
    >>> M = MultiDoop()
    >>> M.addResolution(5,2,mitjana)
    >>> M.addResolution(10,4,mitjana)
    >>>
    >>> m1 = Measure(1,10)
    >>> m2 = Measure(2,10)
    >>> m3 = Measure(5,40) 
    >>> m4 = Measure(10,50)
    >>> m5 = Measure(15,10)
    >>>
    >>>
    >>> M.add(m1)
    >>> M.add(m2)
    >>> M.add(m3)
    >>> M.consolidable()
    True
    >>> M.consolidate_pipe()
    >>> R0,R1 = sorted(M)
    >>> len(R0.D.s)
    2
    >>> len(R1.D.s)
    1
    >>> M.add(m4)
    >>> M.consolidate_pipe()
    >>> R0,R1 = sorted(M)
    >>> len(R0.D.s)
    3
    >>> len(R1.D.s)
    2
    >>> M.add(m5)
    >>> M.consolidate_pipe()
    >>> R0,R1 = sorted(M)
    >>> len(R0.D.s)
    4
    >>> len(R1.D.s)
    2
    """

    def __init__(self):
        super(MultiDoop,self).__init__
        self._s = TimeSeries()
        

    def add(self,m):
        """
        Operació d'afegir una nova mesura a la base de dades
        """
        self._s.add(m)


    def consolidable(self):
        """
        Predicat que indica si hi ha alguna Subsèrie resolució consolidable
        """
        return True


    def consolidate_pipe(self):
        """
        Fa una consolidació a totes les subsèries resolució consolidables
        """
        doop = TsDoopPipe(self._s,self)
        mts = doop.execute()
        self.clear()
        set.update(self,mts)




    def consolidate(self):
        pass
