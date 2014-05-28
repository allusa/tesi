# -*- encoding: utf-8 -*-

#isense

import os.path
import csv
import time, datetime

from roundrobinson import Measure, TimeSeries, MultiresolutionSeriesSharedBuffer
from roundrobinson.aggregators import mean, maximum, mean_zohe, maximum_zohe
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





def consolida_mrd(mrd,temps,valors,debug=False):
    if debug:
        print mrd.str_taus()

    #farciment de mesures amb consolidació
    for t,v in zip(temps,valors):
        m = Measure(t,v)
        mrd.add(m)

        mrd.consolidate()
        if debug:
            print mrd.str_taus()    


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
    mrd = MultiresolutionSeriesSharedBuffer()
    mrd.addResolution(h5,24,mean,zero)
    mrd.addResolution(d2,20,mean,zero)
    mrd.addResolution(d15,12,mean,zero)
    mrd.addResolution(d50,12,mean,zero)

    mrd.addResolution(d50,12,maximum,zero)

    consolida_mrd(mrd,temps,valors,debug)
    return mrd


def crea_mrdzohe(temps,valors,tzero=0,debug=False):

    #temps segons Unix Time Epoch (segons)
    zero = tzero
    h1 = 3600
    h5 = 5 * h1
    d1 = 24 * h1
    d2 = 2 * d1
    d15 = 15 * d1
    d50 = 50 * d1

    #configuració base de dades multiresolució
    mrd = MultiresolutionSeriesSharedBuffer()
    mrd.addResolution(h5,24,mean_zohe,zero)
    mrd.addResolution(d2,20,mean_zohe,zero)
    mrd.addResolution(d15,12,mean_zohe,zero)
    mrd.addResolution(d50,12,mean_zohe,zero)

    mrd.addResolution(d15,12,maximum_zohe,zero)
    mrd.addResolution(d50,12,maximum_zohe,zero)

    consolida_mrd(mrd,temps,valors,debug)
    return mrd



def crea_mrdzohe2(temps,valors,tzero=0,debug=False):

    #temps segons Unix Time Epoch (segons)
    zero = tzero
    h1 = 3600
    h5 = 5 * h1
    d1 = 24 * h1
    d2 = 2 * d1
    d15 = 15 * d1
    d50 = 50 * d1

    #configuració base de dades multiresolució
    mrd = MultiresolutionSeriesSharedBuffer()
    mrd.addResolution(h5,48,mean_zohe,zero)
    mrd.addResolution(d2,40,mean_zohe,zero)
    mrd.addResolution(d15,24,mean_zohe,zero)
    mrd.addResolution(d50,24,mean_zohe,zero)

    mrd.addResolution(d15,24,maximum_zohe,zero)
    mrd.addResolution(d50,24,maximum_zohe,zero)

    consolida_mrd(mrd,temps,valors,debug)
    return mrd

 





if __name__ == '__main__':

    directori = 'matriu0'
    totalmean = os.path.join(directori,'totalmean.csv')
    mrdpickle  = os.path.join(directori,'mrd.pickle')
    isense = 'isense/matriu0.csv'

    print "S'emmagatzemaran dades a {0}/".format(directori)
    if os.path.exists(directori):
        raise Exception("El directori no ha d'existir")
    os.mkdir(directori)
    


    temps,valors = llegeix_dades(isense)
    print "S'ha llegit el fitxer de dades"

    tzero = datetimetotimestamp(datetime.datetime(2010,1,1))
    mrd = crea_mrdzohe(temps,valors,tzero,debug=True)
    print "S'ha farcit i consolidat la base de dades"

    print 'Emmagatzemant dades a {0}/'.format(directori)
    mrd.storage().save_csv(directori)
    mrd.storage().save_pickle(mrdpickle)
    print 'Emmagatzemant unió total a {0}/'.format(totalmean)
    mrd.total(ff=[mean_zohe]).storage().save_csv(totalmean)

    print 'Creant gràfic'
    sp = ScreenPlot(mrd)
    sp.plot()
    #sp.plot_total()
    print 'Gràfic tancat'






