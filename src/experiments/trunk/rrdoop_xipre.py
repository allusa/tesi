


import csv
import datetime

from roundrobindoop import MultiDoopFile
from roundrobinson import TimeSeries, Measure
from roundrobinson.plot import ScreenPlot


def csv2csvtsms(fname,foutput,end=None):


    f = open(fname,'r')
    r = csv.reader(f)

    fo = open(foutput,'w')
    o = csv.writer(fo)

    #headers
    datetimeformat = '%d/%m/%Y %H:%M'
    for l in r:

        try:
            t = datetime.datetime.strptime(l[0],datetimeformat)
            #comencem a llegir dades
            break
        except ValueError:
            #llegim headers
            pass


    headers = {
        't': 's',
        'MathReservoirLevel': 'm',
        'FinAgFotisMath1': 'm3/h',
        'TinAgFotisMath1': 'm3',
        'FinAguliaMath1': 'm3/h',
        'TinAguliaMath1': 'm3',
        'FinAsprMath1': 'm3/h',
        'TinAsprMath1': 'm3',
        'FoutMath1': 'm3/h',
        'ToutMath1': 'm3',
#        '',
        'F_Hi_Math2': 'm3/h',
        'T_Hi_Math2': 'm3',
        'P_Hi_Math2': 'bar',
        'F_Mid_Math2': 'm3/h',
        'T_Mid_Math2': 'm3',
        'P_Mid_Math2': 'bar',
        'F_Lo_Math2': 'm3/h',
        'T_Lo_Math2': 'm3', 
        'P_Lo_Math2': 'bar',
}



    #dades
    pl = parse_csv_line(l)
    o.writerow(pl)
    for l in r:
        pl = parse_csv_line(l)
        if pl[0] == end:
            break
        o.writerow(pl)

    fo.close()
    f.close()


def parse_csv_line(l):
    datetimeformat = '%d/%m/%Y %H:%M'
    datetimeformat2 = '%d/%m/%Y'
    try:
        t = datetime.datetime.strptime(l[0],datetimeformat)
    except ValueError:
        t = datetime.datetime.strptime(l[0],datetimeformat2)

    t = t.strftime('%s')
    vv = l[1:] 
    del vv[9] #columna buida
    v = [ s.replace(',','.') if s != '' else 'nan' for s in vv]

    return [t] + v





def mitjan1(s,i=None):
    pass

def mitjana(s,i=None):
    if len(s) == 0:
        return 0

    if isinstance(s[0][1],list):
        grau = len(s[0][1]) 
    else:
        grau = 1

    sumv = [0] * grau

    for t,v in s:
        if grau == 1:
            sumv[0] += v
        else:
            for i in range(grau):
                sumv[i] += v[i]
        
        
    return ' '.join( str(v/float(len(s))) for v in sumv )



def maxim(s,i):
    v = float("-inf")
    for m in s:
        v = max(v,m[1])         
    return v


def tau_zero(tnow,delta,k):
    return tnow - k*delta - delta



if __name__ == '__main__':

    end = 1409121300

    #csv2csvtsms('/home/aleix/Escriptori/Xipre/xipre2014.csv','xip14.csv', str(end))
  
    m = MultiDoopFile('xip14.csv')
    d1 = 3600 * 24
    m1 = d1 * 30
    m.addResolution(d1,50,mitjana,tau_zero(end,d1,50)) #diaria
    m.addResolution(m1,6,mitjana,tau_zero(end,m1,6)) #mensual

    m.consolidate_pipe()
    p = ScreenPlot(m)
    p.plot()
