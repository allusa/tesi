# -*- encoding: utf-8 -*-

"""
=======
Mesures
=======

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació de les definicions de Mesura.
"""




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
    >>> m1.eqnt(m2)
    False
    >>> m1.eqnt(Measure(1,20))
    False
    >>> m1.eqt(m2)
    False
    >>> m1.eqt(Measure(1,20))
    True
    >>> m1 == m2
    False
    >>> m1 ==  Measure(1,20)
    False
    >>> m1 ==  Measure(1,10)
    True
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
    
    def __eq__(self,other):        
        """
        Relació d'ordre parcial. Cal pensar si també hauria de ser la induïda pel temps i llavors seria total.
        """
        return self.eqnt(other)

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




    def eqnt(self,other):        
        """
        Relació d'igualtat sense tenir en compte el temps
        """
        return isinstance(other,Measure) and self.t == other.t and self.v == other.v

    def eqt(self,other):        
        """
        Relació d'igualtat tenint en compte el temps
        """
        return isinstance(other,Measure) and self.t == other.t


    def isundefinedp(self):
        """
        És cert quan la mesura és indefinida positiva
        """
        return self.t == float("inf") #s'hauria de fer independent

    def isundefinedn(self):
        """
        És cert quan la mesura és indefinida negativa
        """
        return self.t == float("-inf")




class MeasureUndefinedP(Measure):
    """
    Mesura indefinida positiva
    """
    def __init__(self):      
        self.v = float("inf")
        self.t = float("inf")
    
class MeasureUndefinedN(Measure):
    """
    Mesura indefinida negativa
    """
    def __init__(self):      
        self.v = float("inf")
        self.t = float("-inf")
