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
