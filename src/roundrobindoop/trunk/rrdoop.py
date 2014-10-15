#!/usr/bin/env python

"""
Hadoop map-reduce functions for MTSMS
"""


import sys
import datetime
import time
import pickle, marshal, types



#map


def default_parser(l):
    """
    Parses a line of the file in the table format t v and returns a tuple(t,v) where `t` are int and `v` are float or list of floats.

    >>> default_parser("2 10.0")
    (2, 10.0)
    >>> default_parser("2,10.0")
    (2, 10.0)
    >>> default_parser("2 10.0 15.0 20.0")
    (2, [10.0, 15.0, 20.0])
    >>> default_parser("2,10.0,15.0,20.0")
    (2, [10.0, 15.0, 20.0])
    """
    if ',' in l:
        l = l.split(',')
    else:
        l = l.split()


    t = int(l[0])
    if len(l) == 2:
        v = float(l[1])
    else:
        v = [float(e) for e in l[1:] ]

    return (t,v)




def buff_class(t,delta,tau):
    """Resolves Natural `n` in the equation `tau+(n-1)*delta t <= tau+n*delta` and returns `tau+(n)*delta`.


    :type t: int
    :type tau: int
    :type delta: int
    :rtype: int
    
    >>> buff_class(2,5,0)
    5
    >>> buff_class(5,5,0)
    5
    >>> buff_class(6,5,0)
    10
    >>> buff_class(10,5,0)
    10
    >>> buff_class(0,5,0)
    0
    >>> buff_class(-3,5,0)
    0
    >>> buff_class(-5,5,0)
    -5
    >>> buff_class(-6,5,0)
    -5
    """
    #natn = math.ceil((t - tau) / float(delta))
    natn = (tau - t) / delta
    natn = -natn
    return tau + natn * delta


def fname(f):
    try:
        name = f.__name__
    except AttributeError:
        name = f
    return name


def buffer_measure(m,sch,parser_line=None,l=0,g=0):
    """Classifies a measure in the buffers where it belongs
    
    For each delta/f/tau measures (t,v) are classified by the resulting
    consolidation time tb: `tb-delta < t <= tb`

    However, the equation can be parametrised by optional parameters
    `l` and `g` where for each delta/f/tau measures are classified into 
    `tb-(l+1)*delta < t <= tb+g*delta`


    :param m: A measure in a table format t v where t is the time and v is the value
    :type m: str
    :param sch: A multiresolution schema [(delta1,tau1,f1,k1), (delta2,tau2,f2,k2),...]
    
    :param l: an integer for left multiple classification
    :param g: an integer for right multiple classification
    :type l: int
    :type g: int
    
    :return: The measure classification in a table format B t v where B are the buffers
    :rtype: None (prints to stdout)


    >>> sch = [(5,0,'mean',10),(10,0,'mean',5)]
    >>> buffer_measure("2 10.0",sch) # doctest: +NORMALIZE_WHITESPACE
    5/mean-5\t2 10.0
    10/mean-10\t2 10.0
    >>> buffer_measure("6 10.0",sch) # doctest: +NORMALIZE_WHITESPACE
    5/mean-10\t6 10.0
    10/mean-10\t6 10.0
    >>> buffer_measure("6 10.0 15.0 20.0",sch) # doctest: +NORMALIZE_WHITESPACE
    5/mean-10\t6 10.0 15.0 20.0
    10/mean-10\t6 10.0 15.0 20.0

    ## parameters l g
    >>> buffer_measure("2 10.0",sch,l=0,g=0) # doctest: +NORMALIZE_WHITESPACE
    5/mean-5\t2 10.0
    10/mean-10\t2 10.0
    >>> buffer_measure("2 10.0",sch,l=0,g=1) # doctest: +NORMALIZE_WHITESPACE
    5/mean-5\t2 10.0
    10/mean-10\t2 10.0
    >>> buffer_measure("2 10.0",sch,l=1,g=0) # doctest: +NORMALIZE_WHITESPACE
    5/mean-5\t2 10.0
    5/mean-10\t2 10.0
    10/mean-10\t2 10.0
    10/mean-20\t2 10.0
    >>> buffer_measure("6 10.0",sch,l=0,g=1) # doctest: +NORMALIZE_WHITESPACE
    5/mean-10\t6 10.0
    5/mean-5\t6 10.0
    10/mean-10\t6 10.0
    """

    if parser_line is None:
        parser_line = default_parser


    for schema in sch:
        delta,tau,f,k = schema
        t,v = parser_line(m)
        if isinstance(v,list):
            v = ' '.join(str(e) for e in v)


        bclass = buff_class(t,delta,tau)
        #extensio de l'interval
        bclasses = [bclass]
        for i in range(g):
            bclasses.append( bclass-delta*(i+1) )
        for i in range(l):
            bclasses.append( bclass+delta*(i+1) )

        for tb in bclasses:
            if tb <= tau:
                #descartem t <= tau
                continue

            s = "{0}/{1}-{2}\t{3} {4}".format(delta,fname(f),tb,t,v)
            print s



def buffer_ts(f,sch,parser_line=None,lg=[0,0]):
    """
    Classifies the measures of the time series
    
    :param f: A time series in a file-table format t v where t is the time and v is the value
    :type f: A file like format
    :param sch: A multiresolution schema [(delta1,tau1,f1,k1), (delta2,tau2,f2,k2),...]
    :return: Prints to stdout buffer_measure(m,sch) for every m in s

    >>> sch = [(5,0,'mean',10),(10,0,'mean',5)]
    >>> ts = "2 10.0\\n6 10.0"
    >>> fsimulate = ts.split('\\n')
    >>> buffer_ts(fsimulate,sch) # doctest: +NORMALIZE_WHITESPACE
    5/mean-5\t2 10.0
    10/mean-10\t2 10.0
    5/mean-10\t6 10.0
    10/mean-10\t6 10.0
    """
    for line in f:
        line = line.rstrip()
        buffer_measure(line,sch,parser_line,lg[0],lg[1])










#reduce


def reduce_line(l):
    """
    Parses a line of the file in the table format B t v and returns a tuple (delta,f,n,t,v).

    >>> reduce_line("10/mean-0\\t6 10.0")
    ('10', 'mean', 0, 6, 10.0)
    >>> reduce_line("10/mean-0\\t6 10.0 15.0 20.0")
    ('10', 'mean', 0, 6, [10.0, 15.0, 20.0])
    """
    disc,m = l.split('\t')
    delta,fn = disc.split('/')
    f,n = fn.split('-')

    t,v = default_parser(m)


    return (delta,f,int(n),t,v)





def _mean(s):
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



def _convert_to_timeseries(l):
    from roundrobinson import TimeSeries, Measure

    s = TimeSeries()
    for m in l:
        t,v = m
        s.add(Measure(t,v))
    return s

def aggregate(s,f=None,i=None):
    if f is None or isinstance(f,str):
        return _mean(s)

    s = _convert_to_timeseries(s)
    return f(s,i).v


def extract_aggregators(schema):
    aggs = []
    if schema is None:
        return aggs
    for r in schema:
        aggs.append(r[2])

    return aggs

def select_agregator(name,aggs):
    for f in aggs:
        if name == fname(f):
            return f
    


def reduce(f,sch=None):
    """
    >>> f = "10/mean-10\\t2 10.0\\n10/mean-10\\t6 20.0\\n5/mean-5\\t2 10.0\\n5/mean-10\\t6 20.0\\n"
    >>> fsimu = f.split('\\n')
    >>> reduce(fsimu) # doctest: +NORMALIZE_WHITESPACE
    10/mean\t10 15.0
    5/mean\t5 10.0
    5/mean\t10 20.0
    >>>
    >>> f = "10/mean-10\\t2 10.0 15.0 20.0\\n10/mean-10\\t6 20.0 25.0 30.0\\n5/mean-5\\t2 10.0 15.0 20.0\\n5/mean-10\\t6 20.0 25.0 30.0\\n"
    >>> fsimu = f.split('\\n')
    >>> reduce(fsimu) # doctest: +NORMALIZE_WHITESPACE
    10/mean\t10 15.0 20.0 25.0
    5/mean\t5 10.0 15.0 20.0
    5/mean\t10 20.0 25.0 30.0
    """
    previous = None
    ts = []


    aggs = extract_aggregators(sch)


    for line in f:
        line = line.rstrip()
        if line:
            delta,f,n,t,v = reduce_line(line)
            
            if (delta,f,n) == previous:
                ts.append((t,v))
            else:
                if previous is not None:
                    pd,pf,pn = previous 
                    agg = aggregate(ts,f=select_agregator(f,aggs),i=[float(pn)-float(pd),float(pn)])
                    print '{delta}/{f}\t{t} {v}'.format(delta=pd,f=pf,t=pn,v=agg)
                ts = [(t,v)]
                previous = (delta,f,n)

    #last
    if ts:
        agg = aggregate(ts,f=select_agregator(f,aggs),i=[float(n)-float(delta),float(n)])
        print '{delta}/{f}\t{t} {v}'.format(delta=delta,f=f,t=n,v=agg)






def datetimetotimestamp(t):  
    return int(time.mktime(t.timetuple()))


def mrd_schema():

    tzero = datetimetotimestamp(datetime.datetime(2010,1,1))

    #temps segons Unix Time Epoch (segons)
    zero = tzero
    h1 = 3600
    h5 = 5 * h1
    d1 = 24 * h1
    d2 = 2 * d1
    d15 = 15 * d1
    d50 = 50 * d1

    #conf multiresolution data base
    r1 = (h5,zero,'mean',24)
    r2 = (d2,zero,'mean',20)
    r3 = (d15,zero,'mean',12)
    r4 = (d50,zero,'mean',12)

    return [r1,r2,r3,r4]



def mrd_schema_at_time_point(t):

    def tau_zero(tnow,delta,k):
        return tnow - k*delta - delta


    #temps segons Unix Time Epoch (segons)
    tnow = t
    h1 = 3600
    h5 = 5 * h1
    d1 = 24 * h1
    d2 = 2 * d1
    d15 = 15 * d1
    d50 = 50 * d1

    #conf multiresolution data base
    r1 = (h5,tau_zero(tnow,h5,24),'mean',24)
    r2 = (d2,tau_zero(tnow,d2,20),'mean',20)
    r3 = (d15,tau_zero(tnow,d15,12),'mean',12)
    r4 = (d50,tau_zero(tnow,d50,12),'mean',12)

    return [r1,r2,r3,r4]




def despickle_f(f):
    if isinstance(f,str):
        return f

    name,content = f
    code = marshal.loads(content)
    func = types.FunctionType(code, globals(), name)
    return func



def schema_load_pickle(fname):

    from roundrobinson import MultiresolutionSeries
    from roundrobinson.storage import LoadPickle
    
    M = MultiresolutionSeries([])
    M = M.accept(LoadPickle(fname))
    mts = []

    for r in M:
        delta = r.delta()
        tau = r.tau()
        f = r.f()
        k = r.k()
        mts.append((delta,tau,f,k))
    return mts



if __name__ == '__main__':

    tnow = datetimetotimestamp(datetime.datetime(2011,10,18))
    #sch = mrd_schema() #no te en compte k dels discs
    sch = mrd_schema_at_time_point(tnow) #te en compte k dels discs


    def pl(l):
        t,v = l.split(',')

        t = datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
        return (int(t.strftime('%s')),float(v))


    #rrdoop -map|-reduce [-schema e] [-mapl I] [-mapg I]

    if len(sys.argv) > 1:

        if '-schema' in sys.argv:
            pos = sys.argv.index('-schema')
            sch = schema_load_pickle(sys.argv[pos+1])


        if '-map' in sys.argv:
            lg = [0,0]
            if '-mapl' in sys.argv:
                pos = sys.argv.index('-mapl')
                lg[0] = int(sys.argv[pos+1])
            if '-mapg' in sys.argv:
                pos = sys.argv.index('-mapg')
                lg[1] = int(sys.argv[pos+1])

            buffer_ts(sys.stdin,sch,lg=lg)

        elif '-reduce' in sys.argv:
            reduce(sys.stdin,sch)
        elif '-mapdatetime' in sys.argv:
            buffer_ts(sys.stdin,sch,pl)





###Falta definir aggregates generics


#test: cat p.csv | ./rrdoop.py -map | sort -k1,1 | ./rrdoop.py -reduce

#cat roundrobindoop-ts-1393851630.csv | ./rrdoop.py -mapdefault -schema roundrobindoop-ts-1393851630.pickle | sort -k1,1 | ./rrdoop.py -reduce -schema roundrobindoop-ts-1393851630.pickle
