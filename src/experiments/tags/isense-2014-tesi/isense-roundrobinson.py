# -*- encoding: utf-8 -*-


"""

isense amb roundobinson
=======================

Experiment amb les dades d'isense usant RoundRobinson v0.4dev.

"""

import os
import datetime
import csv

from roundrobinson import Measure, TimeSeries, MultiresolutionSeries, MultiresolutionSeriesSharedBuffer
from roundrobinson.aggregators import mean_zohe, maximum_zohe
from roundrobinson.storage import SaveCsvDir, SaveCsv
from roundrobinson.plot import Plot
from roundrobinson.pytsms.representation import Zohe
from roundrobinson.pytsms.storage import SaveCsv as TSSaveCsv, LoadCsv as TSLoadCsv


os.environ['TZ'] = 'UTC' #sinó la conversio strftime es fa amb localtime
CALENDARFORMAT = '%Y-%m-%d %H:%M:%S'
DELIMITER = None

def calendar2timestamp(t):
    t1 = datetime.datetime.strptime(t,CALENDARFORMAT)
    return int(t1.strftime('%s'))




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
tau0 = calendar2timestamp('2010-01-01 00:00:00')
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
#Ajustament dels taus
tmax = '2011-10-18 13:27:59' #darrer temps de la sèrie temporal T(max(S))
M.set_tau_tnow(calendar2timestamp(tmax))
print M.str_taus() #Mostra el temps d'inici


#Afegeix
#S = TimeSeries().accept(TSLoadCsv(original,calendar2timestamp,float))
f = csv.reader(open(fitxer))#,delimiter=' '
for t,v in f:
    M.add(Measure(calendar2timestamp(t),float(v)))
print "S'ha llegit el fitxer de dades"    

#Consolida
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


