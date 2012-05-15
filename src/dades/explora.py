import csv
import datetime
from matplotlib import pyplot


f = csv.reader(open('dades2/taulasensors/matriu0.csv'))


temps = []
valors = []

for t,v in f:
    t = datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    v = float(v)

    temps.append(t)
    valors.append(v)


pyplot.plot(temps,valors)
pyplot.show()
