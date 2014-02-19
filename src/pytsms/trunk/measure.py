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
    :ivar unp: Límit màxim del temps, mesures indefinides positives
    :ivar unn:
    :ivar unv:

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
    >>> m1.eqp(m2)
    False
    >>> m1.eqp(Measure(1,20))
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
    >>>
    >>> Measure(un='p')
    m(inf,None)
    >>> Measure(un='n')
    m(-inf,None)
    >>> Measure(1)
    m(1,None)
    """

    unp=float("inf")
    unn=-float("inf")
    unv=None


    def __init__(self,t=None,v=None,un=None):
        """
        Constructor d'una mesura
        """        
        self.t = t
        self.v = v

        if v is None:
            self.set_undefined('v')

        if un is not None:
            self.set_undefined(un)


    def __gt__(self,other):
        """
        Relació d'ordre més gran induïda pel temps. És la mateixa
        relació tant pel cas parcial com pel total.
        """
        return self.t > other.t 
    
    def __eq__(self,other):        
        """
        Relació d'ordre igualtat parcial induïda pel temps.
        """
        return self.eqp(other)


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





    def partial_order(self,other):
        """
        Relació d'ordre parcial entre mesures

        :type other: :py:class:`Measure`
        :return: m1 ≤ m2 (partial)
        :rtype: boleean

        >>> m1 = Measure(1,1)
        >>> m2 = Measure(1,2)
        >>> m3 = Measure(2,3)
        >>> m4 = Measure(1,1)
        >>> m1.partial_order(m2)
        False
        >>> m2.partial_order(m1)
        False
        >>> m1.partial_order(m3)
        True
        >>> m3.partial_order(m1)
        False
        >>> m1.partial_order(m4)
        True
        """  
        return self.t < other.t or (self.t == other.t and self.v == other.v)

    def total_order(self,other):
        """
        Relació d'ordre total entre mesures

        :type other: :py:class:`Measure`
        :return: m1 ≤ m2 (total)
        :rtype: boleean

        >>> m1 = Measure(1,1)
        >>> m2 = Measure(1,2)
        >>> m3 = Measure(2,3)
        >>> m4 = Measure(1,1)
        >>> m1.total_order(m2)
        True
        >>> m1.total_order(m3)
        True
        >>> m3.total_order(m1)
        False
        >>> m1.total_order(m4)
        True
        """  
        return self.t <= other.t

    def eqp(self,other):        
        """
        Relació d'igualtat parcial
        """
        return isinstance(other,Measure) and self.t == other.t and self.v == other.v

    def eqt(self,other):        
        """
        Relació d'igualtat total o temporal
        """
        return isinstance(other,Measure) and self.t == other.t



    def isundefinedp(self):
        """
        És cert quan la mesura és indefinida positiva

        :rtype: bool

        >>> m1 = Measure(float("inf"),0)
        >>> m1.isundefinedp()
        True
        """
        return self.t == self.unp

    def isundefinedn(self):
        """
        És cert quan la mesura és indefinida negativa

        :rtype: bool

        >>> m1 = Measure(float("-inf"),0)
        >>> m1.isundefinedn()
        True
        """
        return self.t == self.unn


    def isundefined(self):
        """
        És cert quan la mesura és indefinida

        :rtype: bool

        >>> m1 = Measure(float("-inf"),0)
        >>> m2 = Measure(float("inf"),0)
        >>> m3 = Measure(float("inf"),float("nan"))
        >>> m3 = Measure(float("inf"),None)
        >>> m1.isundefined()
        True
        >>> m2.isundefined()
        True
        >>> m3.isundefined()
        True
        """
        return self.isundefinedp() or self.isundefinedn()

    def isvalueundefined(self):
        """
        És cert quan la mesura és de valor indefinit

        :rtype: bool

        >>> m1 = Measure(float("-inf"),0)
        >>> m2 = Measure(float("inf"),None)
        >>> m3 = Measure(2,None)
        >>> m1.isvalueundefined()
        False
        >>> m2.isvalueundefined()
        True
        >>> m3.isvalueundefined()
        True
        """
        return self.v == self.unv


    def set_undefined(self,un):
        """
        Configura la mesura amb indefinicions depenent de `un`:
        
        * 'p' mesura indefinida positiva
        * 'n' mesura indefinida negativa
        * 'v' mesura de valor indefinit
        
        :param un: p|n|v
        :type un: str
        """
        if un=='p':
            self.t = self.unp
        elif un=='n':
            self.t = self.unn
        elif un=='v':
            self.v = self.unv
        else:
            raise ValueError('Incorrect value for parameter un={0}'.format(un))


class MeasureUndefinedP(Measure):
    """
    Mesura indefinida positiva
    """
    def __init__(self):      
        raise DeprecationWarning("Canviat, useu Measure(un='p')")
        self.v = float("inf")
        self.t = float("inf")
    
class MeasureUndefinedN(Measure):
    """
    Mesura indefinida negativa
    """
    def __init__(self):   
        raise DeprecationWarning("Canviat, useu Measure(un='n')")
        self.v = float("inf")
        self.t = float("-inf")




class MeasureFloat(Measure):
    """
    Mesura on el temps i valor són float

    >>> Measure(un='p')
    m(inf,None)
    >>> Measure(un='n')
    m(-inf,None)
    >>> #Measure(1)
    """
    unp=float("inf")
    unn=-float("inf")
    unv=float("nan")


class MeasureChar(Measure):
    """
    Mesura on el temps i valor són char
    """
    unp='z'
    unn='a'
    unv=''
