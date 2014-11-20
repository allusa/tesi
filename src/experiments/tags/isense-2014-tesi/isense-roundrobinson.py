# -*- encoding: utf-8 -*-


"""

isense amb roundobinson
=======================

Experiment amb les dades d'isense usant RoundRobinson v0.4dev.

"""

import os
import time, datetime
import csv

from roundrobinson import Measure, TimeSeries, MultiresolutionSeries, MultiresolutionSeriesSharedBuffer
from roundrobinson.aggregators import mean_zohe, maximum_zohe
from roundrobinson.storage import SaveCsvDir, SaveCsv
from roundrobinson.plot import Plot
from roundrobinson.pytsms.representation import Zohe
from roundrobinson.pytsms.storage import SaveCsv as TSSaveCsv, LoadCsv as TSLoadCsv


def datetimetotimestamp(t):  
    return int(time.mktime(t.timetuple()))

def calendar2timestamp(t):
    t1 = datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    return datetimetotimestamp(t1)


def llegeix_dades(fitxer):

    f = csv.reader(open(fitxer))#,delimiter=' '


    temps = []
    valors = []

    for t,v in f:
        temps.append(calendar2timestamp(t))
        valors.append(float(v))

    return temps,valors


#Directori de dades
original = 'dades/matriu0.csv'
#original = 'dades/matriu0.originalbyday.dat'#experiments
#Directori d'emmagatzematge
directori = 'resultats-ison'
print "S'emmagatzemaran dades a {0}/".format(directori)
if os.path.exists(directori):
    print "El directori {0} no ha d'existir".format(directori)
    exit()
os.mkdir(directori)
    



#Multiresolució
M = MultiresolutionSeriesSharedBuffer()#MultiresolutionSeries()
#Temps en segons, Hora Unix
tau0 = datetimetotimestamp(datetime.datetime(2010,1,1))
h1 = 3600 
h5 = 5 * h1
d1 = 24 * h1
d2 = 2 * d1
d15 = 15 * d1
d50 = 50 * d1
#Esquema de multiresolució
M.addResolution(delta=h5,k=24,f=mean_zohe,tau=tau0)
M.addResolution(delta=d2,k=20,f=mean_zohe,tau=tau0)
M.addResolution(delta=d15,k=12,f=mean_zohe,tau=tau0)
M.addResolution(delta=d50,k=12,f=mean_zohe,tau=tau0)
M.addResolution(delta=d15,k=12,f=maximum_zohe,tau=tau0)
M.addResolution(delta=d50,k=12,f=maximum_zohe,tau=tau0)


#Dades originals
temps,valors = llegeix_dades(original)
#S = TimeSeries().accept(TSLoadCsv(original,calendar2timestamp,float))
print "S'ha llegit el fitxer de dades"

#Afegeix i consolida
print M.str_taus() #Mostra el temps d'inici

for t,v in zip(temps,valors):
    m = Measure(t,v)
    print m.t
    M.add(Measure(t,v))

    M.consolidateTotal(debug=False)
    
print "S'ha farcit i consolidat la base de dades"



#Emmagatzematge
print 'Emmagatzemant dades a {0}/'.format(directori)
M.accept(SaveCsvDir(directori))
M.accept(SaveCsv(os.path.join(directori,'tot.csv')))

#fins aqui per a mesurar el temps!!
exit()

print 'Emmagatzemant total a {0}/'.format(directori)
S1 = M.total(ff=[mean_zohe],rpr=Zohe)
S2 = M.total(ff=[maximum_zohe],rpr=Zohe)
S1.accept(TSSaveCsv(os.path.join(directori,'totalmean.csv')))
S2.accept(TSSaveCsv(os.path.join(directori,'totalmax.csv')))


#Visualització
print 'Creant gràfic'
M.accept(Plot())
S1.set_rpr(Zohe)
S2.set_rpr(Zohe)
S=S1.join(S2)
S.plot()
print 'Gràfic tancat'


