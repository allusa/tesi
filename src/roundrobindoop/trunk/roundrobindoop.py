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
    ...     v = 0
    ...     for m in s:
    ...         v += m[1]         
    ...     return v / float(len(s))
    >>> 
    >>> def maxim(s,i):
    ...     v = float("-inf")
    ...     for m in s:
    ...         v = max(v,m[1])         
    ...     return v
    >>> 
    >>> M = MultiDoop()
    >>> M.addResolution(5,2,mitjana)
    >>> M.addResolution(10,4,maxim)
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
    1
    >>> len(R1.D.s)
    1
    >>> M.add(m4)
    >>> M.consolidate_pipe()
    >>> R0,R1 = sorted(M)
    >>> len(R0.D.s)
    2
    >>> len(R1.D.s)
    1
    >>> M.add(m5)
    >>> M.consolidate_pipe()
    >>> R0,R1 = sorted(M)
    >>> len(R0.D.s)
    3
    >>> len(R1.D.s)
    2
    >>>
    >>> R0.D.s == TimeSeries([Measure(5,20),Measure(10,50),Measure(15,10)])
    True
    >>> R1.D.s == TimeSeries([Measure(10,50),Measure(20,10)])
    True
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



    def empty(self):
        """
        Retorna un nou esquema multiresolució amb els buffers i els discs buits
        """
        mts = type(self)()
        for r in self:
            mts.addResolution(r.delta(),r.k(),r.f(),r.tau())
        
        mts._s = self._s

        return mts



class MultiDoopFile(MultiDoop):
    """
    Especialitació del MultiDoop on es llegeix directament d'un fitxer
    """

    def __init__(self,inputfile=None):
        super(MultiDoop,self).__init__()
        self._s = inputfile


    def add(self,m):
        """
        Operació d'afegir una nova mesura a la base de dades
        """
        pass

