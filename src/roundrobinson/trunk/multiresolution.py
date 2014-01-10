# -*- encoding: utf-8 -*-

"""
=============================
Sèrie temporal multiresolució
=============================

:Abstract: Vegeu document principal `roundrobinson.py`
:Copyright: GPLv3

Implementació de les sèries temporals multiresolució.
"""

from pytsms import TimeSeries
from subseries import ResolutionSubseries

            
class MultiresolutionSeries(set):
    """
    Sèrie temporal multiresolució M = {R0,...,Rd} com un conjunt de
    subsèries resolució

    És una subclasse de set.

    >>> from pytsms import Measure, TimeSeries
    >>>
    >>> def mitjana(s,i):
    ...     sp = s.interval_open_left(i[0],i[1])
    ...     v = sp.aggregate(lambda mi,m: Measure(mi.t+1, mi.v+m.v), Measure(0,0))
    ...     return Measure(i[1], v.v / float(v.t) )
    >>> 
    >>> M = MultiresolutionSeries()
    >>> M.addResolution(5,2,mitjana)
    >>> M.addResolution(10,4,mitjana)
    >>>
    >>> m1 = Measure(1,10)
    >>> m2 = Measure(2,10)
    >>> m3 = Measure(5,40) 
    >>> m4 = Measure(10,50)
    >>> m5 = Measure(15,10)
    >>>
    >>> M.add(m1)
    >>> M.consolidable()
    False
    >>> M.add(m2)
    >>> M.consolidable()
    False
    >>> M.add(m3)
    >>> M.consolidable()
    True
    >>> M.consolidate()
    >>> M.consolidable()
    False
    >>> l = sorted(M)
    >>> R0,R1 = l
    >>> len(R0.B.s) == 0 and R0.B.tau == 5
    True
    >>> len(R1.B.s) == 3 and R1.B.tau == 0
    True
    >>> len(R0.D.s)
    1
    >>> len(R1.D.s)
    0
    >>> M.add(m4)
    >>> M.consolidable()
    True
    >>> M.consolidate()
    >>> M.consolidable()
    False
    >>> len(R0.B.s) == 0 and R0.B.tau == 10
    True
    >>> len(R1.B.s) == 0 and R1.B.tau == 10
    True
    >>> len(R0.D.s)
    2
    >>> len(R1.D.s)
    1
    >>> R0.D.s == TimeSeries([Measure(5,20.0), Measure(10,50)])
    True
    >>> R1.D.s == TimeSeries([Measure(10,27.5)])
    True
    >>> M.add(m5)
    >>> M.consolidable()
    True
    >>> M.consolidate()
    >>> M.consolidable()
    False
    >>> len(R0.B.s) == 0 and R0.B.tau == 15
    True
    >>> len(R1.B.s) == 1 and R1.B.tau == 10
    True
    >>> len(R0.D.s)
    2
    >>> len(R1.D.s)
    1
    >>> R0.D.s == TimeSeries([Measure(15,10.0), Measure(10,50)])
    True
    >>> R1.D.s == TimeSeries([Measure(10,27.5)])
    True
    """

    def addResolution(self,delta,k,f,tau=0):
        """
        Add resolution by delta, k, f and tau
        """
        set.add(self, ResolutionSubseries(delta,k,f,tau) )


    def add(self,m):
        """
        Operació d'afegir una nova mesura a la base de dades
        """
        for R in self:
            R.add(m)

    def consolidable(self):
        """
        Predicat que indica si hi ha alguna Subsèrie resolució consolidable
        """
        for R in self:
            if R.consolidable():
                return True
        return False

    def consolidate(self):
        """
        Fa una consolidació a totes les subsèries resolució consolidables
        """
        for R in self:
            if R.consolidable():
                R.consolidate()


    def consolidateTotal(self, debug=False):
        """
        Consolida iterativament les subsèries mentre la sèrie multiresolució sigui consolidable. Amb debug permet mostrar l'evolució dels instants de consolidació de cada subsèrie

        >>> from pytsms import Measure, TimeSeries
        >>> m1 = Measure(1,10); m2 = Measure(5,10); m3 = Measure(10,40)
        >>> M = MultiresolutionSeries()
        >>> def zero(s,i): return Measure(0,0)
        >>> M.addResolution(5,2,zero)
        >>> M.addResolution(10,4,zero)
        >>> M.add(m1); M.add(m2); M.add(m3)
        >>> M.consolidateTotal(debug=True)
        5/zero:5 | 10/zero:10
        5/zero:10 | 10/zero:10
        """
        while self.consolidable():
            self.consolidate()
            if debug:
                print self.str_taus()



    #Esquema
    def str_taus(self):
        """
        Retorna un string amb el tau de cada subsèrie resolució

        >>> M = MultiresolutionSeries()
        >>> def maxim(s,i): return None
        >>> M.addResolution(5,2,maxim)
        >>> M.addResolution(10,4,maxim)
        >>> M.str_taus()
        '5/maxim:0 | 10/maxim:0'
        """
        l = [ '{0}/{1}:{2}'.format(R.B.delta,R.B.f.__name__,R.B.tau) for R in sorted(self)]
        return ' | '.join(l)


    #CONSULTES
    def discSeries(self,delta,f):
        """
        Retorna la sèrie temporal emmagatzemada de la resolució delta,f

        >>> from pytsms import Measure, TimeSeries
        >>> m1 = Measure(1,10); m2 = Measure(5,10); m3 = Measure(10,40)
        >>> M = MultiresolutionSeries()
        >>> maxim = lambda s,i: max(s[i[0]:i[1]:'c'])
        >>> M.addResolution(5,2,maxim)
        >>> M.addResolution(10,4,maxim)
        >>> M.add(m1); M.add(m2); M.add(m3)
        >>> M.consolidateTotal()
        >>> M.discSeries(5,maxim) == TimeSeries([Measure(5,10),Measure(10,40)])
        True
        >>> M.discSeries(10,maxim) == TimeSeries([Measure(10,40)])
        True
        """
        for R in self:
            if R.B.delta == delta and R.B.f == R.B.f:
                return R.D.s
  

    def total(self,ff=None,rpr=None):
        """
        Retorna la sèrie temporal total que resulta de concatenar les sèries temporals dels discs per ordre de pas de consolidació. Es pot utilitzar la concatenació de seqüències o la concatenació temporal de representació `rpr`. 

        En el cas que hi hagi passos der consolidació repetits, l'ordre és parcial i per tant el resultat és aleatori. Amb `f` es pot seleccionar uns agregadors d'atributs concrets.

        >>> from pytsms import Measure, TimeSeries
        >>> m1 = Measure(1,10); m2 = Measure(5,10); m3 = Measure(10,40)
        >>> m4 = Measure(15,50); m5 = Measure(20,10)
        >>> M = MultiresolutionSeries()
        >>> maxim = lambda s,i: max(s)
        >>> M.addResolution(5,2,maxim)
        >>> M.addResolution(10,4,maxim)
        >>> 
        >>> M.total() == TimeSeries()
        True
        >>> M.add(m1); M.add(m2)
        >>> M.consolidate()
        >>> M.total() == TimeSeries([Measure(5,10)])
        True
        >>> M.add(m3)
        >>> M.consolidate()
        >>> M.total() == TimeSeries([Measure(5,10),Measure(10,40)])
        True
        >>> M.add(m4)
        >>> M.consolidate()
        >>> M.total() == TimeSeries([Measure(15,50),Measure(10,40)])
        True
        >>> M.add(m5)
        >>> M.consolidate()
        >>> M.total() == TimeSeries([Measure(20,10),Measure(15,50),Measure(10,40)])
        True
        >>> from pytsms.representation import Zohe
        >>> M.total(rpr=Zohe) == TimeSeries([Measure(20,10),Measure(15,50),Measure(10,40)])
        True
        >>> M.total(ff=[maxim]) == TimeSeries([Measure(20,10),Measure(15,50),Measure(10,40)])
        True
        >>> M.total(ff=[]) == TimeSeries([])
        True
        >>> M.addResolution(20,1,maxim)
        >>> M.total() == TimeSeries([Measure(20,10),Measure(15,50),Measure(10,40)])
        True
        """ 
        M = self
        if ff is not None:
            M = filter(lambda R: R.B.f in ff,M)
            if len(M) == 0:
                return TimeSeries()

        if rpr is None:
            return reduce(lambda si,rb: si.concatenate(rb.D.s),sorted(M),TimeSeries())
        else:
            return reduce(lambda si,rb: si.concatenate_temporal(rb.D.s,rpr),sorted(M),TimeSeries())


