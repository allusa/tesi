# -*- encoding: utf-8 -*-


import csv
import datetime

from roundrobindoop import MultiDoopFile
from roundrobinson import TimeSeries, Measure, MultiresolutionSeries
from roundrobinson.plot import ScreenPlot
from roundrobinson.pytsms.representation import Zohe





headersORIGINALS = {
#        't': 's',
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

#Atencio els m3 queden convertits a m3/s


headers = [
#        ('t', 's'),
        ('LM', 'm'),
        ('FFotiM1', 'm3/h'),
        ('TFotiM1', 'm3'),
        ('FAgulM1', 'm3/h'),
        ('TAgulM1', 'm3'),
        ('FAsprM1', 'm3/h'),
        ('TAsprM1', 'm3'),
        ('FoM1', 'm3/h'),
        ('ToM1', 'm3'),
#        '',
        ('FhiM2', 'm3/h'),
        ('ThiM2', 'm3/s'),
        ('PhiM2', 'bar'),
        ('FmiM2', 'm3/h'),
        ('TmiM2', 'm3/s'),
        ('PmiM2', 'bar'),
        ('FloM2', 'm3/h'),
        ('TloM2', 'm3/s'), 
        ('PloM2', 'bar'),
        ('LMder', 'm/s'), #computed
]


def headersdict(headers=headers):
    return {tup[0]:i  for i,tup in enumerate(headers)}



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





def mitjana1(s,i=None):
 
    if len(s) == 0:
        return 0
   
    sumv = 0
    for t,v in s:
            sumv += v

    return  sumv/float(len(s))
            


def mitjana1zohe(s,i=None,absolute=False,derive=False):
    """
    si absolute aleshores conversio a velocitat

    >>> s = [(1,1),(2,2),(3,4)]
    >>> mitjana1zohe(s)
    3.0
    >>>
    >>> s = [(1,1),(2,2),(3,4),(4,1),(5,5)]
    >>> mitjana1zohe(s,absolute=True)
    2.0
    """
    if len(s) == 0:
        return float("nan")

    tant = s[0][0]
    vant = s[0][1]

    sumt = 0
    sumv = 0
    for t,v in s:
        deltat = t-tant
        deltav = v - vant

        if deltat == 0:
            area = 0
        elif absolute and deltav < 0:
            area = v
        elif absolute or derive:
            area = deltav
        else:
            area = v * deltat
        sumv += area
        sumt += deltat
        tant = t
        vant = v
        

    return  sumv/float(sumt)


def mitjana1zoheabsolute(s,i=None):           
    return mitjana1zohe(s,i=None,absolute=True)        
def mitjana1zohederive(s,i=None):           
    return mitjana1zohe(s,i=None,derive=True)   


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




def multivalued(s,interval=None,aggs = [],defaultgrau=None):
    """
    >>> s = [(1,[1,2]),(2,[2,3]),(3,[3,4]),(4,[4,5])]
    >>> multivalued(s,aggs=[mitjana1]*4)
    [2.5, 3.5]
    """

    if len(s) == 0:
        if defaultgrau is None:
            return []
        else:
            return [float("nan")] * defaultgrau

    grau = len(s[0][1]) 

    tt = []
    vv = []
    for i in range(grau):
        vv.append( [] )
    
    for t,v in s:
        tt.append(t)
        for i in range(grau):
            vv[i].append(v[i])

    res = []
    for i in range(grau):
        res.append(aggs[i](zip(tt,vv[i]),interval))
    return res

        


def set2timeseries(s):
    ts = TimeSeries()
    for t in s:
        if len(t) == 2:
            ts.add(Measure(t[0],t[1]))
        if len(t) > 2:
            ts.add(Measure(t[0],t[1:]))
    return ts



def ts_multivalued(s,interval=None,aggs = [],defaultgrau=None):
    """
    >>> s = TimeSeries([Measure(1,[1,2]),Measure(2,[2,3]),Measure(3,[3,4]),Measure(4,[4,5])])
    >>> ts_multivalued(s,aggs=[mitjana1]*4)
    [2.5, 3.5]
    """


    if len(s) == 0:
        if defaultgrau is None:
            return []
        else:
            return [float("nan")] * defaultgrau



    grau = 0
    for m in s:
        grau = len(m.v)
        break

    res = []
    for i in range(grau):
        v = 'v{0}'.format(i)
        subs = s.projection(['t',v])
        subs = sorted(set2timeseries(subs))

        res.append(aggs[i](subs,interval))
    return res

        




def maxim(s,i):
    v = float("-inf")
    for m in s:
        v = max(v,m[1])         
    return v


def tau_zero(tnow,delta,k):
    return tnow - k*delta - delta




def robindoop(fname):
    pass
    #m = MultiDoopFile('xip14.csv')
    #m1 = d1 * 30
    #m.addResolution(d1,50,multiaggsdoop,tau_zero(end,d1,50)) #diaria
    #m.addResolution(m1,6,mitjana,tau_zero(end,m1,6)) #mensual


    #m.consolidate_pipe()


def robinson(fname,schema):
    s = TimeSeries()
    def strlist2float(l): return [float(e) for e in l]
    ts = s.storage().load_csv(fname,int,strlist2float)


    m = MultiresolutionSeries()

    for d1,k1,f1 in schema:
        m.addResolution(d1,k1,f1,tau_zero(end,d1,k1)) 

 
    m.update(ts)
    m.consolidateTotal()

    return m



def _timestamp(t): 
    return datetime.datetime.fromtimestamp(t)


def plot(m):
    m.storage().save_dir_csv('xipremrd')
    m.total().storage().save_csv('xipremrd/total.csv')

    p = ScreenPlot(m)
    p.plot()



def _proj(ts,names):
    
    vv = []
    for n in names:
        v = 'v{0}'.format(headersdict()[n])
        vv.append( v )
    
    tp = ts.projection(['t']+vv)
    return set2timeseries(tp)
    



def check1(ts):
    """
    Comprovació ToM1 = ThiM2 + TmiM2 + TloM2
    """
    ts1headers = ['ToM1','ThiM2','TmiM2','TloM2']
    ts1 = _proj(ts,ts1headers)

    
    def sum123(m):
        v = m.v + (m.v[1]+m.v[2]+m.v[3], )
        return Measure(m.t,v)
        

    ts1 = ts1.map(sum123)
    ts1headers.append('SM2')

    ts1.set_rpr(Zohe)
    ts1.rpr().plot(formatx=_timestamp,legend=ts1headers)



def check2(ts):
    """
    Comprovació ToM1, ThiM2, TmiM2, TloM2 (m3/s) vs F (m3/h)
    """
    ts1headers = ['ToM1','ThiM2','TmiM2','TloM2','FoM1','FhiM2','FmiM2','FloM2']
    ts1 = _proj(ts,ts1headers)

    
    def T2F(m):
        h1 = float(3600)
        v = (m.v[0]*h1, m.v[1]*h1, m.v[2]*h1, m.v[3]*h1 ) + m.v [4:]
        return Measure(m.t,v)
        

    ts1 = ts1.map(T2F)

    ts1.set_rpr(Zohe)
    ts1.rpr().plot(formatx=_timestamp,legend=ts1headers)


def check3(ts):
    """
    Comprovació TFotiM1, TAgulM1, TAsprM1 (m3/s) vs F (m3/h)
    """
    ts1headers = ['TFotiM1', 'TAgulM1', 'TAsprM1', 'FFotiM1', 'FAgulM1', 'FAsprM1' ]
    ts1 = _proj(ts,ts1headers)

    def T2F(m):
        h1 = float(3600)
        v = (m.v[0]*h1, m.v[1]*h1, m.v[2]*h1) + m.v [3:]
        return Measure(m.t,v)
        

    ts1 = ts1.map(T2F)

    ts1.set_rpr(Zohe)
    ts1.rpr().plot(formatx=_timestamp,legend=ts1headers)


def check4(ts):
    """
    Comprovació Tin - Tout
    """
    ts1headers = ['ToM1', 'TFotiM1', 'TAgulM1', 'TAsprM1', 'LM', 'LMder' ]
    ts1 = _proj(ts,ts1headers)

    def sum123(m):
        o = m.v[0]
        i = m.v[1] + m.v[2] + m.v[3]
        deltaF = i - o
        v =  ( o , i, deltaF, m.v[4]/float(5000), m.v[5]*100 )
        return Measure(m.t,v)
        

    ts1 = ts1.map(sum123)
    ts1headers = [ 'ToutM1','TinM1', 'DeltaF', 'LM1/5M', 'LMder*100' ]

    ts1.set_rpr(Zohe)
    ts1.rpr().plot(formatx=_timestamp,legend=ts1headers)


def check5(ts):
    """
    Comprovació Level i el seu derive
    """
    ts1headers = ['LM','LMder' ]
    ts1 = _proj(ts,ts1headers)

    def der(m):
        mant = ts1.prev(m)
        if mant.v is None:
            vant = 0
            tant = mant.t
        else:
            vant = mant.v[0]
            tant = mant.t
            
        der = (m.v[0] - vant) / float(m.t - tant)

        v =  ( m.v[0], m.v[1], der)
        return Measure(m.t,v[1:3])
        

    ts1 = ts1.map(der)
    ts1headers = ['LM-2.1','LMder*100','LM1der2' ]

    ts1.set_rpr(Zohe)
    ts1.rpr().plot(formatx=_timestamp,legend=ts1headers)





def consult(fname):
    s = TimeSeries()
    def strlist2float(l): return [float(e) for e in l]
    ts = s.storage().load_csv(fname,int,strlist2float)

    #ts.set_rpr(Zohe)
    #ts.rpr().plot(formatx=_timestamp,legend=headers)

    #check1(ts)
    #check2(ts)
    #check3(ts)
    check4(ts)
    check5(ts)

if __name__ == '__main__':

    end = 1409121300

    #csv2csvtsms('/home/aleix/Escriptori/Xipre/xipre2014.csv','xip14.csv', str(end))
  

    aggs = [
        mitjana1, #'MathReservoirLevel': 'm',
        mitjana1zohe, #'FinAgFotisMath1': 'm3/h',
        mitjana1zoheabsolute, #'TinAgFotisMath1': 'm3',
        mitjana1zohe, #'FinAguliaMath1': 'm3/h',
        mitjana1zoheabsolute, #'TinAguliaMath1': 'm3',
        mitjana1zohe, #'FinAsprMath1': 'm3/h',
        mitjana1zoheabsolute, #'TinAsprMath1': 'm3',
        mitjana1zohe, #'FoutMath1': 'm3/h',
        mitjana1zoheabsolute, #'ToutMath1': 'm3',
#        '',
        mitjana1zohe, #'F_Hi_Math2': 'm3/h',
        mitjana1zoheabsolute, #'T_Hi_Math2': 'm3',
        mitjana1, #'P_Hi_Math2': 'bar',
        mitjana1zohe, #'F_Mid_Math2': 'm3/h',
        mitjana1zoheabsolute, #'T_Mid_Math2': 'm3',
        mitjana1, #'P_Mid_Math2': 'bar',
        mitjana1zohe, #'F_Lo_Math2': 'm3/h',
        mitjana1zoheabsolute, #'T_Lo_Math2': 'm3', 
        mitjana1, #'P_Lo_Math2': 'bar',
        ]

    def multiaggsdoop(s,i):
        return ' '.join( str(v) for v in multivalued(s,i,aggs) )


    def multiaggs(s,i):
        buf = s[i[0]:i[1]:'c']
        v = ts_multivalued(buf,i,aggs,defaultgrau=len(headersORIGINALS))
        #computed
        subs = buf.projection(['t','v0'])
        subs = sorted(set2timeseries(subs))
        v.append(mitjana1zohederive(subs,i))
        return Measure(i[1],v )



    #diaria
    d1 = 3600 * 24
    k1 = 50
    f1 = multiaggs
    #setmanal
    d2 = d1 * 7
    k2 = 20
    f2 = multiaggs
    #schema
    schema = [(d1,k1,f1),(d2,k2,f2)]


    #m = robindoop('xip14.csv',schema)

    #m = robinson('xip14.csv',schema)
    #plot(m)
    #consult('xipremrd/R86400multiaggs.csv')
    consult('xipremrd/total.csv')



