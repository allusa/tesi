# -*- encoding: utf-8 -*-

"""
=======
Mesures
=======

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació de les definicions de Mesura.
"""



class Mesura(object):
    def __init__(self,v,t):
        raise DeprecationWarning("Useu Measure")




class Measure(object):
    """
    Mesura m = (t,v) on v és el valor en el temps t. El temps implementat com a instant de temps. 

    :ivar t: m.t correspon a T(m)
    :ivar v: m.v correspon a V(m) 

    >>> m1 = Measure(1,10)
    >>> m2 = Measure(2,10)
    >>> m1
    m(1,10)
    >>>
    >>> m1 > m2
    False
    >>> m2 > m1
    True
    >>> m1 < m2
    True
    >>> m2 < m1
    False
    >>> m1 == m2
    False
    >>> m1 ==  Measure(1,20)
    True
    >>> m1.eqnt(m2)
    False
    >>> m1.eqnt(Measure(1,20))
    False
    """
    def __init__(self,t,v):
        """
        Constructor d'una mesura
        """        
        self.v = v
        self.t = t

    def __gt__(self,other):
        """
        Relació d'ordre induïda pel temps
        """
        return self.t > other.t 
    
    def eqnt(self,other):        
        """
        Relació d'igualtat sense tenir en compte el temps
        """
        return isinstance(other,Measure) and self.t == other.t and self.v == other.v


    def __eq__(self,other):        
        """
        Relació d'ordre induïda pel temps
        """
        return isinstance(other,Measure) and self.t == other.t

    def __ne__(self,other):
        """
        Relació d'ordre induïda pel temps
        """
        return not self == other




    def __hash__(self):
        """
        Retorna el hash d'una mesura, necessari per poder pertànyer a objectes colleccions com per exemple els sets
        """
        return hash(self.t)
    
    def __repr__(self):
        return 'm({0},{1})'.format(self.t,self.v)
