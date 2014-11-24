# -*- encoding: utf-8 -*-


"""

isense amb roundobindoop
========================

Experiment amb les dades d'isense usant RoundRobindoop.

"""


import os
import time, datetime

from roundrobinson import Measure, TimeSeries, MultiresolutionSeries
from roundrobinson.storage import SavePickle, LoadCsv
from roundrobinson.aggregators import mean_zohe, maximum_zohe
from roundrobinson.plot import Plot
from roundrobinson.pytsms.representation import Zohe
from roundrobinson.pytsms.storage import SaveCsv as TSSaveCsv, LoadCsv as TSLoadCsv 


def datetimetotimestamp(t):  
    return int(time.mktime(t.timetuple()))

def calendar2timestamp(t):
    t1 = datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    return datetimetotimestamp(t1)


#Directori de dades
original = 'dades/matriu0.csv'
#original = 'dades/matriu0.originalbyday.dat' #experiments
#Directori d'emmagatzematge
directori = 'resultats-idoop'
resultat = 'final.csv'
print "S'emmagatzemaran dades a {0}/".format(directori)
if not os.path.exists(directori):
    os.mkdir(directori)



#Multiresolució
M = MultiresolutionSeries()
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

#Emmagatzematge de l'esquema
M.accept(SavePickle(os.path.join(directori,'e.pickle')))


#Execució a la shell
#cat dades/matriu0.csv | roundrobindoop/rrdoop.py -map -schema resultats-idoop/e.pickle -mapg 1 -calendar | sort -k1,1 | roundrobindoop/rrdoop.py -reduce -schema resultats-idoop/e.pickle  > resultats-idoop/final.csv

#Execució a Hadoop
#hadoop dfs -copyFromLocal dades/matriu0.csv /user/aleix/matriu0.csv
#hadoop jar /usr/lib/hadoop/contrib/streaming/hadoop-streaming*.jar -D mapred.reduce.tasks=3 -file roundrobindoop/rrdoop.py -file resultats-idoop/e.pickle  -mapper 'rrdoop.py -map -schema e.pickle -mapg 1 -calendar' -reducer 'rrdoop.py -reduce -schema e.pickle' -input /user/aleix/matriu0.csv -output /user/aleix/final
#hadoop dfs -rmr /user/aleix/final


#Càlcul dels totals, un cop s'ha executat la computació
res = os.path.join(directori,resultat)
if not os.path.exists(res):
    print "Els resultats encara no s'han calculat"
    exit()

def floatwithnones(s):
    if s == 'None':
        return None
    return float(s)
    
Mres = M.accept(LoadCsv(res,int,floatwithnones))

print 'Emmagatzemant total a {0}/'.format(directori)
S1 = Mres.total(ff=[mean_zohe],rpr=Zohe)
S2 = Mres.total(ff=[maximum_zohe],rpr=Zohe)
S1.accept(TSSaveCsv(os.path.join(directori,'totalmean.csv')))
S2.accept(TSSaveCsv(os.path.join(directori,'totalmax.csv')))


#Visualització
print 'Creant gràfic'
Mres.accept(Plot())
S1.set_rpr(Zohe)
S2.set_rpr(Zohe)
S=S1.join(S2)
S.plot()
print 'Gràfic tancat'


