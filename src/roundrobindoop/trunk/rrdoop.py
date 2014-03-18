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
    Parses a line of the file in the table format t v and returns a tuple(t,v) where `t` and `v` are int.

    >>> default_parser("2 10.0")
    (2, 10.0)
    >>> default_parser("2,10.0")
    (2, 10.0)
    """
    if ',' in l:
        t,v = l.split(',')
    else:
        t,v = l.split()

    return (int(t),float(v))




def buff_class(t,delta,tau):
    """
    Resolves Natural `n` in the equation tau+n*delta <= t and returns
    tau+(n+1)*delta

    :type t: int
    :type tau: int
    :type delta: int
    :rtype: int
    
    >>> buff_class(2,5,0)
    5
    >>> buff_class(6,5,0)
    10
    >>> buff_class(-3,5,0)
    0
    >>> buff_class(-6,5,0)
    -5
    """
    natn = (t - tau) / delta
    return tau + (natn+1) * delta





def buffer_measure(m,sch,parser_line=None):
    """
    Classifies a measure in the buffers where it belongs
    
    
    :param m: A measure in a table format t v where t is the time and v is the value
    :type m: str
    :param sch: A multiresolution schema [(delta1,tau1,f1,k1), (delta2,tau2,f2,k2),...]
    :return: The measure classification in a table format B t v where B are the buffers
    :rtype: None (prints to stdout)


    >>> sch = [(5,0,'mean',10),(10,0,'mean',5)]
    >>> buffer_measure("2 10.0",sch) # doctest: +NORMALIZE_WHITESPACE
    5/mean-5\t2 10.0
    10/mean-10\t2 10.0
    >>> buffer_measure("6 10.0",sch) # doctest: +NORMALIZE_WHITESPACE
    5/mean-10\t6 10.0
    10/mean-10\t6 10.0
    """

    if parser_line is None:
        parser_line = default_parser


    for schema in sch:
        delta,tau,f,k = schema
        t,v = parser_line(m)
    
        bclass = buff_class(t,delta,tau)
        if bclass < tau:
            #descartem t < tau
            continue

        s = "{0}/{1}-{2}\t{3} {4}".format(delta,f.__name__,bclass,t,v)
        print s



def buffer_ts(f,sch,parser_line=None):
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
        buffer_measure(line,sch,parser_line)










#reduce


def reduce_line(l):
    """
    Parses a line of the file in the table format B t v and returns a tuple (delta,f,n,t,v).

    >>> reduce_line("10/mean-0\\t6 10.0")
    ('10', 'mean', 0, 6, 10.0)
    """
    disc,m = l.split('\t')
    t,v = m.split()
    delta,fn = disc.split('/')
    f,n = fn.split('-')

    return (delta,f,int(n),int(t),float(v))





def _mean(s):
    if len(s) == 0:
        return 0

    sumv = 0
    for t,v in s:
        sumv += v
        
    return sumv / float(len(s))    



def aggregate(s,f):
    # f=mean
    return _mean(s)



def reduce(f):
    """
    >>> f = "10/mean-10\\t2 10.0\\n10/mean-10\\t6 20.0\\n5/mean-5\\t2 10.0\\n5/mean-10\\t6 20.0\\n"
    >>> fsimu = f.split('\\n')
    >>> reduce(fsimu) # doctest: +NORMALIZE_WHITESPACE
    10/mean\t10 15.0
    5/mean\t5 10.0
    5/mean\t10 20.0
    """
    previous = None
    ts = []

    for line in f:
        line = line.rstrip()
        if line:
            delta,f,n,t,v = reduce_line(line)
            
            if (delta,f,n) == previous:
                ts.append((t,v))
            else:
                if previous is not None:
                    agg = aggregate(ts,f)
                    pd,pf,pn = previous 
                    print '{delta}/{f}\t{t} {v}'.format(delta=pd,f=pf,t=pn,v=agg)
                ts = [(t,v)]
                previous = (delta,f,n)

    #last
    if ts:
        agg = aggregate(ts,f)
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
    name,content = f
    code = marshal.loads(content)
    func = types.FunctionType(code, globals(), name)
    return func

def schema_load_pickle(fname):
        with open(fname,'r') as f:
            mts = pickle.load(f)
            f.close()

        for i,r in enumerate(mts):
            delta,tau,f,k = r
            f = despickle_f(f)
            mts[i] = (delta,tau,f,k)

        return mts




if __name__ == '__main__':

    tnow = datetimetotimestamp(datetime.datetime(2011,10,18))
    #sch = mrd_schema() #no te en compte k dels discs
    sch = mrd_schema_at_time_point(tnow) #te en compte k dels discs


    def pl(l):
        t,v = l.split(',')

        t = datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
        return (int(t.strftime('%s')),float(v))



    if len(sys.argv) > 1:

        if len(sys.argv) == 4:
            if sys.argv[2] == '-schema':
                sch = schema_load_pickle(sys.argv[3])

        if sys.argv[1] == '-map':
            buffer_ts(sys.stdin,sch)
        elif sys.argv[1] == '-reduce':
            reduce(sys.stdin)
        elif sys.argv[1] == '-mapdatetime':
            buffer_ts(sys.stdin,sch,pl)





###Falta definir aggregates generics


#test: cat p.csv | ./rrdoop.py -map | sort -k1,1 | ./rrdoop.py -reduce

#cat roundrobindoop-ts-1393851630.csv | ./rrdoop.py -mapdefault -schema roundrobindoop-ts-1393851630.pickle | sort -k1,1 | ./rrdoop.py -reduce -schema roundrobindoop-ts-1393851630.pickle
