# -*- encoding: utf-8 -*-


####Executar amb python -m dosctest test-ajustamenttaus-roundrobinson.rst


#TEST ROUNDROBINSON


#Importació dels objectes necessaris
>>> from pytsms import TimeSeries, Measure as m
>>> from roundrobinson import MultiresolutionSeries
>>> from roundrobinson.aggregators import mean_zohe,maximum_zohe


#Definició de sèries temporal d'exemple
>>> s = TimeSeries([m(1,6),m(5,2),m(8,5),m(10,0),m(14,1),m(19,6),m(22,11),m(26,6),m(29,0)])

#Definició de la sèrie temporal multiresolució
>>> M = MultiresolutionSeries()

#Definició de l'esquema multiresolució
>>> M.addResolution(delta=5,k=4,f=mean_zohe,tau=0)
>>> M.addResolution(delta=10,k=3,f=maximum_zohe,tau=0)


>>> M.set_tau_tnow(29)
>>> M.str_taus()
'5/mean_zohe:5 | 10/maximum_zohe:-10'

