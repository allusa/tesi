# -*- encoding: utf-8 -*-

#isense

import csv
import time, datetime

from roundrobinson.roundrobinson import MRD
from roundrobinson.serietemporal import Mesura
from roundrobinson.interpoladors import mitjana
from roundrobinson.consultes import consulta
from roundrobinson.operadors import consolidatot, tauactual
from roundrobinson.plot import plot_screen, plot_dir



def datetimetotimestamp(t):  
    return time.mktime(t.timetuple())


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
    mrd = MRD()
    mrd.afegeix_disc(h5,24,mitjana,zero)
    mrd.afegeix_disc(d2,20,mitjana,zero)
    mrd.afegeix_disc(d15,12,mitjana,zero)
    mrd.afegeix_disc(d50,12,mitjana,zero)

    if debug:
        print tauactual(mrd)

    #farciment de mesures amb consolidació
    for t,v in zip(temps,valors):
        m = Mesura(v,t)
        mrd.update(m)

        consolidatot(mrd,debug)

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
    mrd.afegeix_disc(h5,48,mitjana,zero)
    mrd.afegeix_disc(d2,40,mitjana,zero)
    mrd.afegeix_disc(d15,24,mitjana,zero)
    mrd.afegeix_disc(d50,24,mitjana,zero)

    if debug:
        print tauactual(mrd)

    #farciment de mesures amb consolidació
    for t,v in zip(temps,valors):
        m = Mesura(v,t)
        mrd.update(m)

        consolidatot(mrd,debug)

    return mrd







if __name__ == '__main__':


    tzero = datetimetotimestamp(datetime.datetime(2010,1,1))
    temps,valors = llegeix_dades('../../dades/iSense_2010-2011/matriu0.csv')
    print "S'ha llegit el fitxer de dades"
    mrd = crea_mrd(temps,valors,tzero,debug=True)
    print "S'ha farcit i consolidat la base de dades"

    print 'Emmagatzemant dades a matriu0/'
    plot_dir(mrd,'matriu0')

    print 'Creant gràfic'
    plot_screen(mrd)
    print 'Gràfic tancat'





