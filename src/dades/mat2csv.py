#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import os
import sys

import numpy
import scipy.io





def profunditat(nd):
    if len(nd) == 1 or isinstance(nd,numpy.void):
        return 1 + profunditat(nd[0])
        
    return 0

def aplana(nd):
    prof = profunditat(nd)
    dades = nd
    for i in range(prof-1):
        dades = dades[0]
    
    return dades





def processa_mat(mat,directori):

    fitxermat = scipy.io.loadmat(mat,struct_as_record=True)


    if isinstance(fitxermat,dict):
        taules = [(k,fitxermat[k]) for k in fitxermat.keys() if not k.startswith('_')]


    print '{0} taules'.format(len(taules))


    for k,taula in taules:
        subdirectori = os.path.join(directori,'taula'+str(k))
        os.mkdir(subdirectori)
        processa_taula(taula,k,subdirectori)



def processa_taula(taula,nom,directori):
    print 'Taula {0}: {1} matrius'.format(nom,len(taula))
        
    for k,matriu in enumerate(taula):
        fitxer = os.path.join(directori,'matriu{0}.csv'.format(k))
        processa_matriu(matriu,k,fitxer)


def processa_matriu(matriu,num,fitxer):
    prof = profunditat(matriu)
    print 'Matriu {0}: profunditat {1}'.format(num,prof)


    dades = aplana(matriu)
    valors = dades[0]
    temps = dades[1]

    if not len(valors) == len(temps):
        raise Exception('La mida de temps i valors no concorda')

    f = open(fitxer,'w')
    for v,t in zip(valors,temps):
        t = t.strip()
        if isinstance(v,numpy.ndarray):
            v = v[0]

        s = '{0},{1}\n'.format(t,v)
        f.write(s)

    f.close()




def processa_opts(l):

    if len(l) > 3:
        raise Exception('Hi ha massa opcions')
        
    if len(l) < 2:
        raise Exception("Has d'especificar el fitxer mat")

    if len(l) == 2:
        raise Exception("Has d'especificar el directori de sortida")

    if len(l) == 3:
        return (l[1],l[2])
    

    raise Exception()



if __name__ == '__main__':
    
    try: 
        mat,directori = processa_opts(sys.argv)
    except Exception as m:
        print m
        sys.exit()


    if os.path.exists(directori):
        print "Ja existeix un directori dades, esborra'l per continuar"
        sys.exit()
        
    
    os.mkdir(directori)


    processa_mat(mat,directori)
