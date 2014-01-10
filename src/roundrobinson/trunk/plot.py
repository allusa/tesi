# -*- encoding: utf-8 -*-

"""
Multiresolution database plot tools
"""
import os

from pytsms import Measure, TimeSeries

import datetime
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator


def _test_crea_mrd(temps,valors,tzero=0,debug=False):

    from multiresolution import MultiresolutionSeries as MRD
    from aggregators import mean, maximum_zohe

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

    mrd.addResolution(h5,24,mean,zero)
    mrd.addResolution(d2,20,mean,zero)
    mrd.addResolution(d15,12,mean,zero)
    mrd.addResolution(d50,12,mean,zero)

    if debug:
        print mrd.str_taus()

    #farciment de mesures amb consolidació
    for t,v in zip(temps,valors):
        m = Measure(t,v)
        mrd.add(m)

    mrd.consolidateTotal(debug)

    return mrd


def _test_crea_mrd2(temps,valors,tzero=0,debug=False):

    from multiresolution import MultiresolutionSeries as MRD
    from aggregators import mean, maximum_zohe

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

    mrd.addResolution(h5,24,mean,zero)
    mrd.addResolution(d2,20,mean,zero)
    mrd.addResolution(d15,12,mean,zero)
    mrd.addResolution(d50,12,mean,zero)

    mrd.addResolution(h5,24,maximum_zohe,zero)

    if debug:
        print mrd.str_taus()

    #farciment de mesures amb consolidació
    for t,v in zip(temps,valors):
        m = Measure(t,v)
        mrd.add(m)

    mrd.consolidateTotal(debug)

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


def plot_coordinates(st):
    """
    Set of tuples (time formated,value) points for a time series.  

    :param st: Time Series
    :returns: Set of tuples formated for plotting
    :rtype: List of tuples

    >>> m1 = Measure(0,5); m2 = Measure(1,6)
    >>> s = TimeSeries([m1,m2])
    >>> plot_coordinates(s)
    [('1970-01-01 00:00:00', '5'), ('1970-01-01 00:00:01', '6')]
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




class ScreenPlot(object):
    """
    Dibuixa una sèrie temporal multiresolució per pantalla amb el matplotlib
    """

    def __init__(self,mrd):
        self._mrd = mrd

    def plot_total(self):
        """
        Pinta les subsèries resolució d'una sèrie multiresolució

        >>> ut = 3600
        >>> mrd = _test_crea_mrd2([ut*x for x in [1,5,10,15,20,48,96]],[1,2,3,4,5,6,7])
        >>> sp = ScreenPlot(mrd)
        >>> #sp.plot_total()
        """
        #figura amb tota la MRD
        interpoladors = set()
        for rd in self._mrd:
            interpoladors.add(rd.B.f)

        #pintem per cada interpolador en el mateix gràfic
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(1,1,1)

        for interpolador in interpoladors:
            sttot = self._mrd.total(ff=[interpolador])
            vt = []
            vv = []
            while len(sttot):
                m = min(sttot)
                sttot.discard(m)
                temps = datetime.datetime.fromtimestamp(m.t)
                vt.append(temps)
                vv.append(m.v)

            ax2.plot(vt,vv,label=interpolador.__name__)

        ax2.legend()
        plt.show()


    def plot(self):
        """
        Pinta els discs resolució d'una base de dades multiresolució

        >>> ut = 3600
        >>> mrd = _test_crea_mrd2([ut*x for x in [1,5,10,15,20,48,96]],[1,2,3,4,5,6,7])
        >>> sp = ScreenPlot(mrd)
        >>> #sp.plot()
        """
        #pinta
        #import locale
        #locale.setlocale(locale.LC_TIME, '') #activa els locales per defecte
        fig = plt.figure(dpi=40)#figsize=(1,1)) #dpi=80 -> 80x80px


        mida = len(self._mrd)
        index = 1


        #plot dades originals
        #pyplot.plot(temps,valors)

        #plot dades discs
        mrdordenat = sorted(self._mrd)

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
            etiqueta = "{0}/{2} |{1}|".format(_timestamptostring(rd.B.delta),rd.D.k,rd.B.f.__name__)

            ax.plot(vt,vv,label=etiqueta)
            ax.legend()

        ax.xaxis.set_label_text('Temps')


        #fig.autofmt_xdate()
        plt.show()




class FilePlot(object):
    """
    Write a mrd into filesytem

    >>> ut = 3600
    >>> mrd = _test_crea_mrd2([ut*x for x in [1,5,10,15,20,48,96]],[1,2,3,4,5,6,7])
    >>> fp = FilePlot(mrd)
    >>> #os.mkdir('exemple')
    >>> #fp.plot_dir('exemple')
    >>> #fp.plot_dir_total('exemple')
    """

    def __init__(self,mrd):
        self._mrd = mrd

    def plot_file_coordinates(self,st,f):
        """
        Write in a file  time,value points for a time series.  

        :param st: Time Series
        :param f: Opened for writring file
        :type f: File
        """
        for t,v in plot_coordinates(st):
            s = '{0},{1}\n'.format(t,v)
            f.write(s)


    def _plot_file_rd_min(self,rd,f):
        """
        Write first unknown (infinite) value from the resolution disc
        """
        delta = rd.B.delta
        st = rd.D.s

        if len(st) == 0:
            return

        mmin = min(st) 
        minf = Measure(mmin.t-delta, float('inf'))
        sinf = TimeSeries()
        sinf.add(minf)

        self.plot_file_coordinates(sinf,f)


    def plot_dir(self,dirc,basename=''):
        """
        Write a mrd values into a filesystem. Directory `dirc`must be created.

        :param dirc: Directory name
        :type dirc: string
        :param basename: Base name for files
        :type basename: string
        """
        for i,rd in enumerate(sorted(self._mrd)):
            nom = '{0}{1}.csv'.format(basename,i)
            f = open(os.path.join(dirc,nom),'w')


            delta = rd.B.delta
            interpolador = rd.B.f.__name__
            cardinal = rd.D.k
            cap = '# RD: {0}s |{1}| {2}\n'.format(delta,cardinal,interpolador)
            f.write(cap)

            self._plot_file_rd_min(rd,f)
            self.plot_file_coordinates(rd.D.s,f)

            f.close()


    def plot_dir_total(self,dirc,basename='total'):
        """
        Write a mrd total operation values into a filesystem.
        Total is the all concatenation for every interpolator.

        :param dirc: Directory name
        :type dirc: string
        """
        #figura amb tota la MRD
        interpoladors = set()
        for rd in self._mrd:
            interpoladors.add(rd.B.f)

        #pintem per cada interpolador en el mateix gràfic
        for i,interpolador in enumerate(interpoladors):
            sttot = self._mrd.total([interpolador])

            nom = '{0}{1}.csv'.format(basename,i)
            f = open(os.path.join(dirc,nom),'w')

            interpoladornom = interpolador.__name__
            cap = '# TS: consult all {0}\n'.format(interpoladornom)
            f.write(cap)
            self.plot_file_coordinates(sttot,f)

            f.close()



class PgfPlot(object):
    """
    LaTeX pgfplotv1.6 code for a mrd.
    """

    def __init__(self,mrd):
        self._mrd = mrd


    def plot_latex_coordinates(self,st):
        """
        LaTeX pgfplot piece code for a time series.  

        :param rd: Time Series
        :rtype: string
        >>> ut = 3600
        >>> mrd = _test_crea_mrd([ut*x for x in [1,5,10,15,20,48,96]],[1,2,3,4,5,6,7])
        >>> pp = PgfPlot(mrd)
        >>> mrdo = sorted(mrd)
        >>> print pp.plot_latex_coordinates(mrdo[1].D.s)
                   (1970-01-03 00:00:00,3.5)
                   (1970-01-05 00:00:00,7.0)
        <BLANKLINE>
        >>> print pp.plot_latex_coordinates(mrdo[0].D.s)
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
        >>> print pp.plot_latex_coordinates(mrdo[2].D.s)
                   (1970-01-01 00:00:00,0)
                   (1970-01-02 00:00:00,1)
        <BLANKLINE>
        """
        s = ''
        for t,v in plot_coordinates(st):
            s += '           ({0},{1})\n'.format(t,v)
        return s


    def plot_latex_rd(self,rd):
        """
        LaTeX pgfplot piece code for a resolution disc.

        :param rd: Resolution Disc
        :rtype: string

        >>> ut = 3600
        >>> mrd = _test_crea_mrd([ut*x for x in [1,5,10,15,20,48,96]],[1,2,3,4,5,6,7])
        >>> pp = PgfPlot(mrd)
        >>> mrdo = sorted(mrd)
        >>> pp.plot_latex_rd(mrdo[2])
        '%% delta 0 k 12 aggregator mean: no data\\n'
        """

        st = rd.D.s    

        if len(st) == 0:
            return '%% delta {0} k {2} aggregator {1}: no data\n'.format(rd.B.tau,rd.B.f.__name__,rd.D.k)


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
        s += self.plot_latex_coordinates(st)

        #tancament
        s += '     };\n'

        s += """
      \end{axis}
    \end{tikzpicture}
    """

        return s

    def plot(self):
        """
        LaTeX pgfplotv1.6 code for a mrd.

        :rtype: string

        >>> ut = 3600
        >>> mrd = _test_crea_mrd2([ut*x for x in [1,5,10,15,20,48,96]],[1,2,3,4,5,6,7]) 
        >>> pp = PgfPlot(mrd)
        >>> #print pp.plot()
        """
        s = ''
        for rd in sorted(self._mrd):
            s += self.plot_latex_rd(rd)
            s += '\n'
        return s

