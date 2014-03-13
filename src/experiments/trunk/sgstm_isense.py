# -*- encoding: utf-8 -*-

#isense

import os.path
import csv
import time, datetime

from roundrobinson import Measure, TimeSeries, MultiresolutionSeries
from roundrobinson.aggregators import mean, maximum
from roundrobinson.plot import ScreenPlot




def datetimetotimestamp(t):  
    return time.mktime(t.timetuple())


def llegeix_serietemporal(fitxer):
    
    def _todatetime(s):
        t = datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S')
        return datetimetotimestamp(t)

    s = TimeSeries()
    return s.storage().load_csv(fitxer,_todatetime,float)




def llegeix_dades(fitxer):

    f = csv.reader(open(fitxer))


    temps = []
    valors = []

    for t,v in f:
        t = datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
        v = float(v)

        temps.append(datetimetotimestamp(t))
        valors.append(v)

    return temps,valors


def crea_mrd(temps,valors,tzero=0,debug=False):

    #temps segons Unix Time Epoch (segons)
    zero = tzero
    h1 = 3600
    h5 = 5 * h1
    d1 = 24 * h1
    d2 = 2 * d1
    d15 = 15 * d1
    d50 = 50 * d1

    #configuració base de dades multiresolució
    mrd = MultiresolutionSeries()
    mrd.addResolution(h5,24,mean,zero)
    mrd.addResolution(d2,20,mean,zero)
    mrd.addResolution(d15,12,mean,zero)
    mrd.addResolution(d50,12,mean,zero)

    mrd.addResolution(d50,12,maximum,zero)



    if debug:
        print mrd.str_taus()

    #farciment de mesures amb consolidació
    for t,v in zip(temps,valors):
        m = Measure(t,v)
        mrd.add(m)

        mrd.consolidateTotal(debug)

    return mrd


def crea_mrd2(temps,valors,tzero=0,debug=False):

    #temps segons Unix Time Epoch (segons)
    zero = tzero
    h1 = 3600
    h5 = 5 * h1
    d1 = 24 * h1
    d2 = 2 * d1
    d15 = 15 * d1
    d50 = 50 * d1

    #configuració base de dades multiresolució
    mrd = MRD()
    mrd.afegeix_disc(h5,48,zohed_arithmetic_mean,zero)
    mrd.afegeix_disc(d2,40,zohed_arithmetic_mean,zero)
    mrd.afegeix_disc(d15,24,zohed_arithmetic_mean,zero)
    mrd.afegeix_disc(d50,24,zohed_arithmetic_mean,zero)

    mrd.afegeix_disc(d50,24,zohed_maximum,zero)

    if debug:
        print tauactual(mrd)

    #farciment de mesures amb consolidació
    for t,v in zip(temps,valors):
        m = Mesura(v,t)
        mrd.update(m)

        consolidatot(mrd,debug)

    return mrd







if __name__ == '__main__':

    directori = 'matriu0'
    roriginal = os.path.join(directori,'original.csv')
    totalmean = os.path.join(directori,'totalmean.csv')
    mrdpickle  = os.path.join(directori,'mrd.pickle')

    print "S'emmagatzemaran dades a {0}/".format(directori)
    if os.path.exists(directori):
        raise Exception("El directori no ha d'existir")
    os.mkdir(directori)
    

    tzero = datetimetotimestamp(datetime.datetime(2010,1,1))
    temps,valors = llegeix_dades('isense/matriu0.csv')
    s = llegeix_serietemporal('isense/matriu0.csv')
    s.storage().save_csv(roriginal)
    import sys
    sys.exit()
    print "S'ha llegit el fitxer de dades"
    mrd = crea_mrd(temps,valors,tzero,debug=True)
    print "S'ha farcit i consolidat la base de dades"

    print 'Emmagatzemant dades a {0}/'.format(directori)
    mrd.storage().save_csv(directori)
    mrd.storage().save_pickle(mrdpickle)
    print 'Emmagatzemant unió total a {0}/'.format(totalmean)
    mrd.total(ff=[mean]).storage().save_csv(totalmean)

    print 'Creant gràfic'
    sp = ScreenPlot(mrd)
    sp.plot()
    #sp.plot_total()
    print 'Gràfic tancat'






