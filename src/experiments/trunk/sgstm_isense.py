# -*- encoding: utf-8 -*-

#isense

import csv
import time, datetime

from roundrobinson.roundrobinson import MRD
from roundrobinson.serietemporal import Mesura
from roundrobinson.interpoladors import mitjana

import locale

from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter


def datetimetotimestamp(t):  
    return time.mktime(t.timetuple())

def tauactual(mrd):
    taus = []
    for rd in mrd:
        taus.append( datetime.datetime.fromtimestamp(rd.B.tau).strftime("%d/%m/%y") )
    return taus

def consolidatot(mrd,debug=False):
     while mrd.consolidable():
        mrd.consolida()
        if debug:
            print tauactual(mrd)
 


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
    d1 = 24 * h1
    d5 = 5 * d1
    m1 = 30 * d1

    #configuració base de dades multiresolució
    mrd = MRD()
    mrd.afegeix_disc(h1,48,mitjana,zero)
    mrd.afegeix_disc(d1,10,mitjana,zero)
    mrd.afegeix_disc(d5,10,mitjana,zero)
    mrd.afegeix_disc(m1,15,mitjana,zero)

    if debug:
        print tauactual(mrd)

    #farciment de mesures amb consolidació
    for t,v in zip(temps,valors):
        m = Mesura(v,t)
        mrd.update(m)

        consolidatot(mrd,debug)

    return mrd



def dibuixa(mrd):
    """
    Pinta els discs resolució d'una base de dades multiresolució

    >>> ut = 3600
    >>> mrd = crea_mrd([ut*x for x in [1,2,3,4,5,24,48]],[1,2,3,4,5,6,7])
    >>> dibuixa(mrd)
    """


    #pinta
    locale.setlocale(locale.LC_TIME, '')
    fig = plt.figure()
    format = DateFormatter('%d/%m')

    mida = len(mrd)
    index = 1


    #plot dades originals
    #pyplot.plot(temps,valors)

    #plot dades discs
    #millor ordenar els discs per delta
    mrdordenat = []
    while mrd:
        deltamin = None
        for rd in mrd:
            if deltamin is None or rd.B.delta < deltamin:
                deltamin = rd.B.delta
                rdmin = rd
        mrdordenat.append(rdmin)
        mrd.remove(rdmin)

    for index,rd in enumerate(mrdordenat):
        st = rd.D.s
        vt = []
        vv = []
        antt = None
        while len(st):
            m = min(st)
            st.discard(m)

            #plot zohe
            valor = m.v
            temps = datetime.datetime.fromtimestamp(m.t)
            if antt:
                vt.append(antt)
                vv.append(valor)
            vt.append(temps)
            vv.append(valor)

            antt = temps


        if len(vt) == 0:
            #plot future delta
            vt.append( datetime.datetime.fromtimestamp(rd.B.tau+rd.B.delta))
            #vv.append(float("inf"))
            vv.append(0)

        if len(vt) == 1:
            #plot point
            vt = vt[0]
            vv = vv[0]

        #print vt,vv

        ax = fig.add_subplot(mida,1,index+1)
        ax.grid(True)
        ax.yaxis.set_label_text(u'Temp. (\u2103)')
        #ax.xaxis.set_major_formatter(format)
        plt.xticks(rotation=20)
        fig.subplots_adjust(hspace=0.8)
        etiqueta = "DR: d {0} c {1}".format(rd.B.delta,rd.D.k)
        
        ax.plot(vt,vv,label=etiqueta)
        ax.legend()

    ax.xaxis.set_label_text('Temps')

    #fig.autofmt_xdate()
    plt.show()



if __name__ == '__main__':


    tzero = datetimetotimestamp(datetime.datetime(2010,1,1))
    temps,valors = llegeix_dades('../../dades/iSense_2010-2011/matriu0.csv')
    print "S'ha llegit el fitxer de dades"
    mrd = crea_mrd(temps,valors,tzero,debug=True)
    print "S'ha farcit i consolidat la base de dades"
    print 'Creant gràfic'
    dibuixa(mrd)
    print 'Gràfic tancat'





