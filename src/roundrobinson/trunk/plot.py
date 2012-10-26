# -*- encoding: utf-8 -*-

"""
Multiresolution database plot tools
"""
import os

from consultes import consulta
from operadors import tauactual

import datetime
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator


def _test_crea_mrd(temps,valors,tzero=0,debug=False):

    from roundrobinson import MRD
    from serietemporal import Mesura
    from interpoladors import mitjana, zohed_maximum
    from operadors import consolidatot

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

    mrd.afegeix_disc(h5,24,zohed_maximum,zero)

    if debug:
        print tauactual(mrd)

    #farciment de mesures amb consolidació
    for t,v in zip(temps,valors):
        m = Mesura(v,t)
        mrd.update(m)

        consolidatot(mrd,debug)

    return mrd



def _timestamptostring(t):
    
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


def _formatador(delta):
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



def plot_screen(mrd):
    """
    Pinta els discs resolució d'una base de dades multiresolució

    >>> ut = 3600
    >>> mrd = _test_crea_mrd([ut*x for x in [1,5,10,15,20,48,96]],[1,2,3,4,5,6,7])
    >>> #plot_screen(mrd)
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
    #import locale
    #locale.setlocale(locale.LC_TIME, '') #activa els locales per defecte
    fig = plt.figure(dpi=40)#figsize=(1,1)) #dpi=80 -> 80x80px


    mida = len(mrd)
    index = 1


    #plot dades originals
    #pyplot.plot(temps,valors)

    #plot dades discs
    mrdordenat = sorted(mrd)

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
        format = DateFormatter(_formatador(rd.B.delta))
        ax.xaxis.set_major_formatter(format)
        locatx = MaxNLocator(8)
        locaty = MaxNLocator(4)
        ax.xaxis.set_major_locator(locatx)
        ax.yaxis.set_major_locator(locaty)
        plt.xticks(rotation=15)
        fig.subplots_adjust(hspace=0.5)
        etiqueta = "RD: {0} |{1}|".format(_timestamptostring(rd.B.delta),rd.D.k)
        
        ax.plot(vt,vv,label=etiqueta)
        ax.legend()

    ax.xaxis.set_label_text('Temps')


    #fig.autofmt_xdate()
    plt.show()





def plot_coordinates(st):
    """
    Set of tuples (time formated,value) points for a time series.  

    :param st: Time Series
    :returns: Set of tuples formated for plotting
    :rtype: List of tuples
    """
    s = []

    if len(st) == 0:
        t = datetime.datetime.utcfromtimestamp(0)
        t2 = datetime.datetime.utcfromtimestamp(3600*24)
        s.append((t,0))
        s.append((t2,1))

    for m in sorted(st):
        t = datetime.datetime.utcfromtimestamp(m.t)#temps UTC
        v = str(m.v)
        # if v == float('inf'):
        #     v = 0
        t = t.strftime('%Y-%m-%d %H:%M:%S')
        s.append((t,v))

    return s


def plot_file_coordinates(st,f):
    """
    Write in a file  time,value points for a time series.  

    :param st: Time Series
    :param f: Opened for writeing file
    :type f: File
    """
    for t,v in plot_coordinates(st):
        s = '{0},{1}\n'.format(t,v)
        f.write(s)

def plot_dir(mrd,dirc):
    """
    Write a mrd values into a filesystem

    :param f: Directory name
    :type f: string
    """
    if os.path.exists(dirc):
        raise Exception('Directory name exists')

    os.mkdir(dirc)
    for i,rd in enumerate(sorted(mrd)):
        nom = '{0}.csv'.format(i)
        f = open(os.path.join(dirc,nom),'w')
        plot_file_coordinates(rd.D.s,f)
        f.close()


def plot_latex_coordinates(st):
    """
    LaTeX pgfplot piece code for a time series.  

    :param rd: Time Series
    :rtype: string
    >>> ut = 3600
    >>> mrd = _test_crea_mrd([ut*x for x in [1,5,10,15,20,48,96]],[1,2,3,4,5,6,7])
    >>> mrdo = llista_ordenada(mrd)
    >>> print plot_latex_coordinates(mrdo[1].D.s)
               (1970-01-03 00:00:00,3.5)
               (1970-01-05 00:00:00,7.0)
    <BLANKLINE>
    >>> print plot_latex_coordinates(mrdo[0].D.s)
               (1970-01-01 05:00:00,1.5)
               (1970-01-01 10:00:00,3.0)
               (1970-01-01 15:00:00,4.0)
               (1970-01-01 20:00:00,5.0)
               (1970-01-02 01:00:00,inf)
               (1970-01-02 06:00:00,inf)
               (1970-01-02 11:00:00,inf)
               (1970-01-02 16:00:00,inf)
               (1970-01-02 21:00:00,inf)
               (1970-01-03 02:00:00,6.0)
               (1970-01-03 07:00:00,inf)
               (1970-01-03 12:00:00,inf)
               (1970-01-03 17:00:00,inf)
               (1970-01-03 22:00:00,inf)
               (1970-01-04 03:00:00,inf)
               (1970-01-04 08:00:00,inf)
               (1970-01-04 13:00:00,inf)
               (1970-01-04 18:00:00,inf)
               (1970-01-04 23:00:00,inf)
    <BLANKLINE>
    >>> print plot_latex_coordinates(mrdo[2].D.s)
               (1970-01-01 00:00:00,0)
               (1970-01-02 00:00:00,1)
    <BLANKLINE>
    """

    s = ''

    for t,v in plot_coordinates(st):
        s += '           ({0},{1})\n'.format(t,v)


    return s


def plot_latex_rd(rd):
    """
    LaTeX pgfplot piece code for a resolution disc.

    :param rd: Resolution Disc
    :rtype: string
    """

    st = rd.D.s    

    if len(st) == 0:
        return '\n'


    #obertura
    s = """\\begin{tikzpicture}
    \\begin{axis}[
        width = \\textwidth,
        height = 3.5cm,
        date coordinates in=x,
"""

    zero = datetime.datetime.utcfromtimestamp(rd.B.delta)
    s += '        date ZERO={0},\n'.format(zero)

    s += """        xticklabel style= {rotate=15,anchor=east},
        xlabel=temps (UTC),
        x label style={anchor=north west},
        ylabel=quantitat (bytes),
        ]
"""    


    s += '     \\addplot[blue] coordinates{\n'


    #mig    
    s += plot_latex_coordinates(st)

    #tancament
    s += '     };\n'

    s += """
  \end{axis}
\end{tikzpicture}
"""

    return s

def plot_latex(mrd):
    """
    LaTeX pgfplotv1.6 code for a mrd.

    :rtype: string

    >>> ut = 3600
    >>> mrd = _test_crea_mrd([ut*x for x in [1,5,10,15,20,48,96]],[1,2,3,4,5,6,7])
    >>> #plot_latex(mrd)
    """

    s = ''

    for rd in sorted(mrd):
        s += plot_latex_rd(rd)
        s += '\n'

    return s




if __name__ == '__main__':
    ut = 3600
    mrd = _test_crea_mrd([ut*x for x in [1,5,10,15,20,48,96]],[1,2,3,4,5,6,7])
    print plot_latex(mrd)
    #plot_dir(mrd,'exemple')
