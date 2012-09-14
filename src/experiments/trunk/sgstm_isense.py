# -*- encoding: utf-8 -*-

#isense

import csv
import time, datetime

from roundrobinson.roundrobinson import MRD
from roundrobinson.serietemporal import Mesura
from roundrobinson.interpoladors import mitjana
from roundrobinson.consultes import consulta

import locale

from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator


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
 

def timestamptostring(t):
    
    s1 = 1
    h1 = 3600
    d1 = 24 * h1
    m1 = 30 * d1
    y1 = 365 * d1

    if t%y1 == 0 and t/y1 != 0:
        return '{0}y'.format(t/y1)
    if t%m1 == 0 and t/m1 != 0:
        return '{0}m'.format(t/m1)
    if t%d1 == 0 and t/d1 != 0:
        return '{0}d'.format(t/d1)
    if t%h1 == 0 and t/h1 != 0:
        return '{0}h'.format(t/h1)
        
    return '{0} s'.format(t)


def formatador(delta):
    """
    Retorna el millor format per a representar temps que que
    provinguin d'aquest delta
    """

    strftimes = {
        's': '%X',
        'h': '%H:%M',
        'd': '%b %d',
        'm': '%b %Y',
        'y': '%Y',
        }
    
    s1 = 1
    h1 = 3600
    d1 = 24 * h1
    m1 = 30 * d1
    y1 = 365 * d1  


    ut = None
    if delta > y1:
        ut = 'y'
    elif delta > m1:
        ut = 'm'
    elif delta > d1:
        ut = 'd'
    elif delta > h1:
        ut = 'h'
    elif delta > s1:
        ut = 's'     

    if ut in strftimes:
        return strftimes[ut]
    return '%c'



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



def dibuixa(mrd):
    """
    Pinta els discs resolució d'una base de dades multiresolució

    >>> ut = 3600
    >>> mrd = crea_mrd([ut*x for x in [1,5,10,15,20,48,96]],[1,2,3,4,5,6,7])
    >>> dibuixa(mrd)
    """

    #figura amb tota la MRD
    sttot = consulta(mrd)
    vt = []
    vv = []
    while len(sttot):
        m = min(sttot)
        sttot.discard(m)
        temps = datetime.datetime.fromtimestamp(m.t)
        vt.append(temps)
        vv.append(m.v)

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(1,1,1)
    ax2.plot(vt,vv,label='MRD')





    #pinta
    #locale.setlocale(locale.LC_TIME, '') #activa els locales per defecte
    fig = plt.figure(dpi=40)#figsize=(1,1)) #dpi=80 -> 80x80px


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
        #ax.yaxis.set_label_text(u'Temp. (\u2103)')
        format = DateFormatter(formatador(rd.B.delta))
        ax.xaxis.set_major_formatter(format)
        locatx = MaxNLocator(8)
        locaty = MaxNLocator(4)
        ax.xaxis.set_major_locator(locatx)
        ax.yaxis.set_major_locator(locaty)
        plt.xticks(rotation=15)
        fig.subplots_adjust(hspace=0.5)
        etiqueta = "RD: {0} |{1}|".format(timestamptostring(rd.B.delta),rd.D.k)
        
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





