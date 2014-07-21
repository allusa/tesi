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
from storage import MultiresolutionStorage
            


class VisitableMixin():
    def accept(self, visitor):
        return visitor(self)


class MultiresolutionSeries(VisitableMixin,set):
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

    def getResolution(self,delta,f):
        """
        Get resolution by delta, f
        """
        for r in self:
            if r.delta() == delta and r.f() == f:
                return r

    def add(self,m):
        """
        Operació d'afegir una nova mesura a la base de dades
        """
        for R in self:
            R.add(m)

    def update(self,s):
        """
        Operació d'afegir les mesures d'una sèrie temporal, en general d'un iterable, a la base de dades

        :param s: A Time series or an iterable (list, set, etc.)
        :type s: Iterable

        >>> from pytsms import Measure,TimeSeries
        >>> s = TimeSeries([Measure(1,2),Measure(2,3)])
        >>> l = [Measure(3,2),Measure(4,3)]
        >>> m = MultiresolutionSeries()
        >>> m.addResolution(5,2,'mean')
        >>> m.update(s)
        >>> m.update(l)
        >>> r0 = sorted(m)[0]
        >>> r0.B.s ==  TimeSeries([Measure(1,2),Measure(2,3),Measure(3,2),Measure(4,3)])
        True
        """
        for m in s:
            self.add(m)


    def consolidable(self):
        """
        Predicat que indica si hi ha alguna Subsèrie resolució consolidable
        """
        for R in self:
            if R.consolidable():
                return True
        return False

    def consolidate(self,rm=True):
        """
        Fa una consolidació a totes les subsèries resolució consolidables

        :param rm: if True removes old measures in buffer
        :type rm: bool
        """
        for R in self:
            if R.consolidable():
                R.consolidate()
        if rm:
            self.rm_olds()

        

    def rm_olds(self):
        """
        Elimina les mesures velles de totes les subsèries resolució
        """
        for R in self:            
            R.B.rm_olds()



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
        0 5/zero:5 | 10/zero:10
        1 5/zero:10 | 10/zero:10
        """
        i = 0
        while self.consolidable():
            self.consolidate()
            if debug:
                print i, self.str_taus()
                i += 1


    #Esquema

    def schema_eq(self,other):
        """
        Relació d'igualtat d'esquema multiresolució

        >>> M = MultiresolutionSeries()
        >>> def maxim(s,i): return None
        >>> M.addResolution(5,2,maxim)
        >>> M.addResolution(10,4,maxim)
        >>> M2 = MultiresolutionSeries()
        >>> def maxim(s,i): return None
        >>> M2.addResolution(5,2,maxim)
        >>> M2.addResolution(10,4,maxim)
        >>> M.schema_eq(M2)
        True
        >>> #Igualtat total
        >>> M == M2
        True
        >>> from pytsms.measure import Measure
        >>> M.add(Measure(1,2))
        >>> M == M2
        False
        >>> M2.add(Measure(1,2))
        >>> M == M2
        True
        """
        for r1 in self:
            eq = False
            for r2 in other: 
                if r1.schema_eq(r2):
                    eq = True
                    break
            if eq == False:
                return False
        return True

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


    def seriedisc(self,delta,f):
        """
        Alias for discseries
        """
        return self.discseries(delta,f)

    def totalseries(self):
        """
        Alias for total
        """
        return self.totalseries()




    def storage(self):
        """
        Retorna un objecte amb totes les operacions d'emmagatzematge al disc

        :deprecated: Use Visitable/Visitor Pattern

        >>> M = MultiresolutionSeries()
        >>> isinstance(M.storage(), MultiresolutionStorage)
        DEPRECATED: Use Visitor Pattern
        True
        """
        return MultiresolutionStorage(self)


    def empty(self):
        """
        Retorna un nou esquema multiresolució amb els buffers i els discs buits
        """
        mts = type(self)()
        for r in self:
            mts.addResolution(r.delta(),r.k(),r.f(),r.tau())
        return mts



    def set_tau_tnow(self,tnow):
        """
        Set tau of each resolution to a time that ignores old measures that will not be in the resulting consolidation as the would immediately be discarded
        """
        for R in self:
            R.set_tau_tnow(tnow)




class MultiresolutionSeriesSharedBuffer(MultiresolutionSeries):
    """
    Sèrie temporal multiresolució M = {R0,...,Rd} on les subsèries resolució comparteixen el buffer


    >>> from pytsms import Measure, TimeSeries
    >>>
    >>> def mitjana(s,i):
    ...     sp = s.interval_open_left(i[0],i[1])
    ...     v = sp.aggregate(lambda mi,m: Measure(mi.t+1, mi.v+m.v), Measure(0,0))
    ...     return Measure(i[1], v.v / float(v.t) )
    >>> 
    >>> M = MultiresolutionSeriesSharedBuffer()
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
    >>> len(R0.B.s) == len(R1.B.s) and R0.B.tau == 5
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
    >>> len(R0.B.s) == len(R1.B.s)  and R0.B.tau == 10
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
    >>> len(R0.B.s) == len(R1.B.s)  and R0.B.tau == 15
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
    def __init__(self):
        super(MultiresolutionSeries,self).__init__()
        self.B = TimeSeries()
        self.Btau = None

    def addResolution(self,delta,k,f,tau=0):
        """
        Add resolution by delta, k, f and tau
        """
        r = ResolutionSubseries(delta,k,f,tau)
        r.B.s = self.B
        set.add(self, r)


    def add(self,m):
        """
        Operació d'afegir una nova mesura a la base de dades
        """
        self.B.add(m)
        
    def update(self,s):
        """
        Operació d'afegir les mesures d'una sèrie temporal
        """
        self.B.update(s)
        

    def rm_olds(self):
        """
        Elimina les mesures velles de totes les subsèries resolució
        """
        taus = [R.B.tau for R in self]
        mtau = min(taus)

        if self.Btau is None or self.Btau < mtau:
            nous = self.B[mtau::'l']
            self.B.clear()
            self.B.update(nous)
            self.Btau = mtau

