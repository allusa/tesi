# -*- encoding: utf-8 -*-

"""
=============
RoundRobinson
=============

:Author: Aleix Llusà Serra
:Contact: aleix@dipse.upc.edu
:Version: 0.2-dev
:Date: 	2012-09-06
:Abstract: Implementació en Python d'un SGBD per sèries temporals multiresolució (SGSTM). Python implementation for a Multiresolution Time Series DBMS (MTSMS).
:Copyright: GPLv3

Implementació en Python d'un SGBD per sèries temporals multiresolució
(SGSTM). És la implementació de referència del model de dades SGSTM
descrit a http://escriny.epsem.upc.edu/projects/rrb/

Amb el suport de la Universitat Politècnica de Catalunya (UPC).
"""


from serietemporal import Mesura, SerieTemporal
from discbuffer import Buffer, Disc, ResolutionDisc
from interpoladors import mitjana, area
                
            
class MRD(set):
    """
    Base de dades multiresolució M = {R0,...,Rd} com un conjunt de
    discs resolució

    És una subclasse de set.

    >>> M = MRD()
    >>> M.afegeix_disc(5,2,mitjana)
    >>> M.afegeix_disc(10,4,mitjana)
    >>>
    >>> m1 = Mesura(10,1)
    >>> m2 = Mesura(10,2)
    >>> m3 = Mesura(40,5) 
    >>> m4 = Mesura(50,10)
    >>> m5 = Mesura(10,15)
    >>>
    >>> M.update(m1)
    >>> M.consolidable()
    False
    >>> M.update(m2)
    >>> M.consolidable()
    False
    >>> M.update(m3)
    >>> M.consolidable()
    True
    >>> M.consolida()
    >>> M.consolidable()
    False
    >>> M
    MRD([RD:Buffer(SerieTemporal([m(10,1), m(10,2), m(40,5)]),0,10),Disc(SerieTemporal([]), |4|), RD:Buffer(SerieTemporal([]),5,5),Disc(SerieTemporal([m(20.0,5)]), |2|)])
    >>> M.update(m4)
    >>> M.consolidable()
    True
    >>> M.consolida()
    >>> M.consolidable()
    False
    >>> M
    MRD([RD:Buffer(SerieTemporal([]),10,10),Disc(SerieTemporal([m(27.5,10)]), |4|), RD:Buffer(SerieTemporal([]),10,5),Disc(SerieTemporal([m(20.0,5), m(50.0,10)]), |2|)])
    >>> M.update(m5)
    >>> M.consolidable()
    True
    >>> M.consolida()
    >>> M.consolidable()
    False
    >>> M
    MRD([RD:Buffer(SerieTemporal([m(10,15)]),10,10),Disc(SerieTemporal([m(27.5,10)]), |4|), RD:Buffer(SerieTemporal([]),15,5),Disc(SerieTemporal([m(50.0,10), m(10.0,15)]), |2|)])
    """

    def __init__(self):
         set.__init__(self)

    def afegeix_disc(self,delta,k,f,tau=None):
        self.add( ResolutionDisc(delta,k,f,tau) )

    def update(self,m):
        """
        Operació d'afegir una nova mesura a la base de dades
        """
        for R in self:
            R.afegeix(m)

    def consolidable(self):
        """
        Predicat que indica si hi ha algun Disc Resolució consolidable
        """
        for R in self:
            if R.consolidable():
                return True
        return False

    def consolida(self):
        for R in self:
            if R.consolidable():
                R.consolida()



    
