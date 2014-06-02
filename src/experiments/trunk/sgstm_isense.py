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



def dades2timeseries(fitxer):

    s = TimeSeries()

    def readtime(t):
        return datetimetotimestamp(datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S'))

    ts = s.storage().load_csv(fitxer,ttype=readtime,vtype=float)

    return ts




def consolida_mrd(mrd,tlast):

    if tlast is not None:
        mrd.set_tau_tnow(tlast)

    if debug:
        print mrd.str_taus()

    mrd.consolidateTotal(debug=True)




def crea_mrd(tzero=0,tlast=None):

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

    return mrd


def crea_mrdzohe(tzero=0,tlast=None):

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

    return mrd



def crea_mrdzohe2(tzero=0,tlast=None,):

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

    return mrd

 





if __name__ == '__main__':

    directori = 'matriu0'
    totalmean = os.path.join(directori,'totalmean.csv')
    tspickle  = os.path.join(directori,'tsoriginal.pickle')
    mrdpickle  = os.path.join(directori,'mrd.pickle')
    tsoriginal = 'isense/original-tsms.csv'

    print "S'emmagatzemaran dades a {0}/".format(directori)
    if os.path.exists(directori):
        raise Exception("El directori no ha d'existir")
    os.mkdir(directori)
    

    isense = 'isense/matriu0.csv'
    #temps,valors = llegeix_dades(isense)
    ts = dades2timeseries(isense)
    print "S'ha llegit el fitxer de dades"
    ts.storage().save_pickle(tspickle)
    print ts
    exit() 
    ts = TimeSeries()
    ts = ts.storage().load_pickle(tsoriginal)


    tzero = datetimetotimestamp(datetime.datetime(2010,1,1))
    tlast = datetimetotimestamp(datetime.datetime(2011,10,18))
    mrd = crea_mrdzohe(tzero,tlast)
    mrd.update(ts)
    print "S'ha farcit la base de dades"
    consolida_mrd(mrd,tlast)
    print "S'ha consolidat la base de dades"

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






