# -*- encoding: utf-8 -*-


####Executar amb python -m dosctest test-roundrobinson.rst



#TEST PYTSMS


#Importació dels objectes necessaris
>>> from pytsms import TimeSeries, Measure as m
>>> from pytsms.representation import Zohe
>>> from pytsms.properties import isRegular

#Definició de les dues sèries temporals d'exemple
>>> s1 = TimeSeries([ m(1,1), m(3,1), m(4,0), m(5,1) ])
>>> s2 = TimeSeries([ m(2,2), m(3,2), m(4,0), m(6,2) ])

#Manipulacions de les dues sèries temporals
# æ$s_1 \glssymbol{not:sgst:cup} s_2$æ
>>> s1.union(s2)
TimeSeries([m(1,1), m(2,2), m(3,1), m(4,0), m(5,1), m(6,2)])

# æ$s_1 \glssymbol{not:sgst:cupt} s_2$æ
>>> s1.union_temporal(s2)
TimeSeries([m(1,1), m(2,2), m(4,0), m(5,1), m(6,2)])

# æ$s_1 \glssymbol{not:sgst:concatenate} s_2$æ
s1.concatenate(s2) 
TimeSeries([m(1,1), m(3,1), m(4,0), m(5,1), m(6,2)])

# æ$s_2[2,5]$æ
>>> s2.interval_closed(2,5)
TimeSeries([m(2,2), m(3,2), m(4,0)])

# æ$s_2[2,5]^{\glssymbol{not:zohe}}$æ
>>> s2.interval_temporal(2,5,Zohe)
TimeSeries([m(3,2), m(4,0), m(5,2)])

#Comprovació de la regularitat
# æ$s_2$æ no és regular
>>> s2.accept(isRegular())
False

# regularitzem æ$s_2$æ amb la selecció temporal æ$s_2[{0,2,4}]^{\glssymbol{not:zohe}}$æ
>>> r2 = s2.selection_temporal([0,2,4],Zohe)
>>> r2
TimeSeries([m(0,2), m(2,2), m(4,0)])
>>> r2.accept(isRegular())
True

Gràfic de la sèrie temporal æ$s_2$æ amb representació æ\gls{zohe}æ
>>> s2.plot(rpr=Zohe)

[æv.~\autoref{fig:python:plotzohe}æ]




#Importació dels objectes necessaris
>>> from pytsms.storage import SaveCsv, LoadCsv

#Emmagatzematge en format æ\gls{CSV}æ de nom st2.csv
>>> s2.accept(SaveCsv('st2.csv'))

#Recuperació a partir de format æ\gls{CSV}æ
>>> sr = TimeSeries([])
>>> sr.accept(LoadCsv('st2.csv'))
TimeSeries([m(2,2), m(3,2), m(4,0), m(6,2)])





#TEST ROUNDROBINSON


#Importació dels objectes necessaris
>>> from pytsms import TimeSeries, Measure as m
>>> from roundrobinson import MultiresolutionSeries
>>> from roundrobinson.aggregators import mean_zohe,maximum_zohe
>>> from roundrobinson.plot import Plot
>>> from pytsms.representation import Zohe


#Definició de sèries temporal d'exemple
>>> s = TimeSeries([m(1,6),m(5,2),m(8,5),m(10,0),m(14,1),m(19,6),m(22,11),m(26,6),m(29,0)])

#Definició de la sèrie temporal multiresolució
>>> M = MultiresolutionSeries()

#Definició de l'esquema multiresolució
>>> M.addResolution(delta=5,k=4,f=mean_zohe,tau=0)
>>> M.addResolution(delta=10,k=3,f=maximum_zohe,tau=0)

#Addició de totes les mesures de la sèrie temporal
>>> for m in s: M.add(m)

#M ja és consolidable
>>> M.consolidable()
True

#Consolidació fins que no sigui consolidable
>>> while M.consolidable(): M.consolidate()

#Consulta æ$\glssymbol{not:sgstm:seriedisc}(M,5,\glssymbol{not:sgstm:meanzohe})$æ
>>> M.discSeries(5,mean_zohe)
TimeSeries([m(10,3), m(15,2), m(20,7), m(25,8)])

#Consulta æ$\glssymbol{not:sgstm:seriedisc}(M,10,\glssymbol{not:sgstm:maxzohe})$æ
>>> M.discSeries(10,maximum_zohe)
TimeSeries([m(10,6), m(20,11)])

#Consulta æ$\glssymbol{not:sgstm:serietotal}(M)$æ
>>> M.total()
TimeSeries([m(10,3), m(15,2), m(20,7), m(25,8)])

#Gràfic multiresolució
>>> M.accept(Plot())

[æv.~\autoref{fig:python:BDMm}æ]

#Gràfic Pytsms de la sèrie temporal total amb representació æ\gls{zohe}æ
>>> M.total().plot(rpr=Zohe)

[æv.~\autoref{fig:python:BDMmtotal}æ]





#Importació dels objectes necessaris
>>> from roundrobinson.storage import SavePickle, LoadPickle, SaveCsv, LoadCsv

#Emmagatzematge en format Pickle de nom mrd.pickle
>>> M.accept(SavePickle('mrd.pickle'))

#Recuperació a partir de format Pickle
>>> Mr = MultiresolutionSeries([])
>>> Mr = Mr.accept(LoadPickle('mrd.pickle'))
>>> Mr == M
True

#Emmagatzematge en format æ\gls{CSV}æ de nom mrd.csv
>>> M.accept(SaveCsv('mrd.csv'))

#Recuperació a partir de format æ\gls{CSV}æ
>>> Mr = M.accept(LoadCsv('mrd.csv'))



