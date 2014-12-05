# -*- encoding: utf-8 -*-


####Executar amb python -m dosctest roundrobindoop.rst

>>> import os
>>> from pytsms import TimeSeries, Measure as m
>>> from roundrobinson import MultiresolutionSeries
>>> from roundrobinson.storage import SavePickle, SaveCsv, LoadCsv
>>> from pytsms.storage import SaveCsv as TSSaveCsv
>>> from roundrobinson.aggregators import mean_zohe,maximum_zohe

#Definició de sèries temporal d'exemple
>>> s = TimeSeries([m(1,6),m(5,2),m(8,5),m(10,0),m(14,1),m(19,6),m(22,11),m(26,6),m(29,0)])


#Definició de la sèrie temporal multiresolució
>>> M = MultiresolutionSeries()

#Definició de l'esquema multiresolució
>>> M.addResolution(delta=5,k=4,f=mean_zohe,tau=0)
>>> M.addResolution(delta=10,k=3,f=maximum_zohe,tau=0)


#Emmagatzematge en format Pickle de nom e.pickle
>>> M.accept(SavePickle('e.pickle'))

#Emmagatzematge en format CSV de nom original.csv
>>> s.accept(TSSaveCsv('original.csv'))





#Executar en bash:

cat original.csv | ./rrdoop.py -map -schema e.pickle -mapg 1 | sort -k1,1 | ./rrdoop.py -reduce -schema e.pickle  > final.csv



#Recuperació en format CSV de nom final.csv
>>> if os.path.exists('final.csv'): Mr = M.accept(LoadCsv('final.csv',int,lambda x: None if x=='None' else float(x),mtype=m))
>>> Mr.getResolution(5,mean_zohe).sd() == TimeSeries([m(5,2.8), m(10,3.0), m(15,2.0), m(20,7.0), m(25,8.0), m(30,None) ])
True
>>> Mr.getResolution(10,maximum_zohe).sd() == TimeSeries([m(10,6.0), m(20,11.0), m(30,None) ])
True
