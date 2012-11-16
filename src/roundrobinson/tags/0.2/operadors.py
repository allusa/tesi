# -*- encoding: utf-8 -*-

import datetime




def tauactual(mrd):
    taus = []
    for rd in mrd:
        taus.append( datetime.datetime.fromtimestamp(rd.B.tau).strftime("%Y-%m-%d") )
    return taus

def consolidatot(mrd,debug=False):
     while mrd.consolidable():
        mrd.consolida()
        if debug:
            print tauactual(mrd)



def llista_ordenada(mrd):
    """
    Deprecated! use sorted(mrd)
    Ordena els discs de la mrd per delta
    
    :deprecated:
    :param: Deprecated!
    :return: Deprecated! 
    :rtype: list
    """   
    # mrdordenat = []
    # while mrd:
    #     deltamin = None
    #     for rd in mrd:
    #         if deltamin is None or rd.B.delta < deltamin:
    #             deltamin = rd.B.delta
    #             rdmin = rd
    #     mrdordenat.append(rdmin)
    #     mrd.remove(rdmin)

    # return mrdordenat
    return sorted(mrd)


def sel_interpolador(mrd,f):
    """
    Selecciona de la `mrd` els discs resolució que tinguin l'interpolador `f`.

    :type f: `function`
    :rtype: `MRD`

    >>> from plot import _test_crea_mrd2
    >>> from interpoladors import mitjana, zohed_maximum, zohed_arithmetic_mean
    >>> ut = 3600
    >>> mrd = _test_crea_mrd2([ut*x for x in [1,5,10,15,20,48,96]],[1,2,3,4,5,6,7])
    >>> r = sel_interpolador(mrd,mitjana)
    >>> len(r)
    4
    >>> r2 = sel_interpolador(mrd,zohed_maximum)
    >>> len(r2)
    1
    >>> r3 = sel_interpolador(mrd,zohed_arithmetic_mean)
    >>> len(r3)
    0
    >>> r3
    MRD([])
    """
    res = mrd.copy()
    for rd in mrd:
        if rd.B.f != f:
            res.remove(rd)

    return res



def ts_decimate_day(st):
    """
    Decimate a time series by selecting max and min for each day timestamp
    """
    pass
    #de moment sense temps (hores minuts segons)
    # tant = None
    # for t,v in zip(temps,valors):
    #     if tant is None or t.date() != tant.date():
    #         s += '           ({0},{1})\n'.format(t.strftime('%Y-%m-%d'),v) 
            
    #     tant = t
