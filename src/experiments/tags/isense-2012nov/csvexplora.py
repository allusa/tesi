
# -*- encoding: utf-8 -*-

"""
CSV PARSER

"""


import sys
import csv
import datetime
from matplotlib import pyplot
import numpy





def read_csv(nom):
    f = csv.reader(open(nom))

    temps = []
    valors = []
    mitjana = 0

    for t,v in f:
        t = datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
        v = float(v)

 
        temps.append(t)
        valors.append(v)
        mitjana += v
        


 

    return temps, valors


def statistics(temps,valors):
    mida = len(temps)
    avalors = numpy.array(valors)

    return (mida,avalors.mean(),avalors.std())    


def print_statistics(temps,valors):
    s = "Mida: {0[0]} mostres\nMitjana: {0[1]}\nStdDev: {0[2]}"
    print s.format(statistics(temps,valors))

def plot_screen(temps,valors):

    pyplot.plot(temps,valors)

    st = statistics(temps,valors)
    ymin = st[1] - 3*st[2]
    ymax = st[1] + 3*st[2]
    pyplot.ylim(ymin, ymax)
    pyplot.show()


def pgfplot(temps,valors):
    s = """\\begin{tikzpicture}
    \\begin{axis}[
        date coordinates in=x,
        xticklabel style= {rotate=15,anchor=east},
        xlabel=temps,
        x label style={anchor=north west},
        ylabel=quantitat (bytes),
        ]
       \\addplot[blue] coordinates{
"""

    #de moment sense temps (hores minuts segons)
    tant = None
    for t,v in zip(temps,valors):
        if tant is None or t.date() != tant.date():
            s += '           ({0},{1})\n'.format(t.strftime('%Y-%m-%d'),v) 
            
        tant = t

        
    
    s += """
        };
  \end{axis}
\end{tikzpicture}"""

    return s



def decimate(temps,valors):
    """
    Fes una decimació per tal que hi hagi un punt cada dia
    """
    #intercanvia entre min(False) i max(True)
    ext = min

    s = ''
    tant = temps[0]
    vant = valors[0]
    for t,v in zip(temps,valors):
        if tant.date() == t.date():
            vant = ext(vant,v)
        else:
            s += '{0} {1}\n'.format(tant.strftime('%Y-%m-%d'),vant)
            tant = t
            vant = v
            if ext is min:
                ext = max
            else:
                ext = min

    s += '{0} {1}\n'.format(tant.strftime('%Y-%m-%d'),vant)


    return s


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Indica el fitxer'
        sys.exit()

    temps, valors = read_csv(sys.argv[1])

    if len(sys.argv) == 2:
        print_statistics(temps,valors)
        plot_screen(temps,valors)

    if len(sys.argv) > 2 and sys.argv[2] == 'latex':
        print pgfplot(temps,valors)


    # file.csv decimate out.dat
    if len(sys.argv) > 2 and sys.argv[2] == 'decimate':
        if len(sys.argv) == 4:
            ftx = sys.argv[3]
            s = decimate(temps,valors)
            f = open(ftx,'a')
            f.write(s)
            f.close()
        else:
            print decimate(temps,valors)
