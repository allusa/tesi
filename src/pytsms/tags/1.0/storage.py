# -*- encoding: utf-8 -*-

"""
=======
Storage
=======

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació d'operacions d'emmagatzematge al disc per a les sèries temporals

Diferents formats:

    * pickle
    * csv

"""



import pickle
import csv

from measure import Measure



class Storage(object):
    """
    Per a emmagatzemar i recuperar del disc

    Les subclasses són visitors i, sigui `s=TimeSeries()` es criden com:

    * s.accept( Storage() )
    * o bé Storage()(s)

    """
    def __init__(self, fname):
        self.fname = fname



class SavePickle(Storage):
    """
    Un visitor
    """
    def __call__(self,ob):
        with open(self.fname,'w') as f:
            pickle.dump(ob,f)
            f.close()
 
class LoadPickle(Storage):
    """
    Un visitor

    >>> from timeseries import TimeSeries
    >>> from measure import Measure
    >>> s = TimeSeries([Measure(1,2), Measure(3,4)])
    >>> f = _doctest_file()
    >>> s.accept( SavePickle(f) )
    >>> ns = s.accept( LoadPickle(f) )
    >>> s == ns
    True
    >>> _doctest_file_rm(f)
    True
    """  
    def __call__(self, ob):
        with open(self.fname, 'r') as f:
            ts = pickle.load(f)
            f.close()

        return ts




class SaveCsv(Storage):
    """
    Un visitor

    S'emmagatzemen ordenades per temps
    """
    def __call__(self,ob):
        with open(self.fname,'w') as f:
            csvwriter = csv.writer(f)
            for m in sorted(ob):
                if isinstance(m.v, list):
                    cv = [m.t] + m.v
                else:
                    cv = [m.t,m.v]
                csvwriter.writerow(cv)
            f.close()


class LoadCsv(Storage):
    """
    Un visitor

    Recuperador a partir d'un fitxer en format CSV. En el fittxer els
    valors desats són strings, en cas que es vulgui convertir-los
    cal indicar el tipus amb `ttype` i `vtype`.

    :type fname: str
    :type ttype: type
    :type vtype: type
    :type mtype: type(Measure)

    >>> from timeseries import TimeSeries
    >>> from measure import Measure
    >>> s = TimeSeries([Measure(1,2), Measure(3,4)])
    >>> f = _doctest_file()
    >>> s.accept(SaveCsv(f))
    >>> ns = s.accept(LoadCsv(f,int,int))
    >>> s == ns
    True
    >>> _doctest_file_rm(f)
    True
    >>> 
    >>> s = TimeSeries([Measure(1,[2,3]), Measure(3,[4,5])])
    >>> f = _doctest_file()
    >>> s.accept(SaveCsv(f))
    >>> def strlist2int(l): return [int(e) for e in l]
    >>> ns = s.accept(LoadCsv(f,int,strlist2int))
    >>> s == ns
    True
    >>> _doctest_file_rm(f)
    True
    """
    def __init__(self,fname,ttype=None,vtype=None,mtype=Measure):
        super(Storage,self).__init__()
        self.fname = fname
        self.ttype = ttype
        self.vtype = vtype
        self.mtype = mtype

    def _parser_row(self,row):
        if len(row) == 2:
            t,v = row
        else:
            t = row[0]
            v = row[1:]

        if self.ttype is not None:
            t = self.ttype(t)
        if self.vtype is not None:
            v = self.vtype(v)

        return self.mtype(t,v)
        
    def __call__(self,ob):
        ts = ob.empty()
        with open(self.fname,'r') as f:
            csvreader = csv.reader(f)

            for row in csvreader:
                ts.add(self._parser_row(row))

            f.close()

        return ts







class TimeSeriesStorage(object):
    """
    Objecte que agrupa les operacions d'emmagatzematge al disc en diferents formats:

    * pickle
    * csv

    :deprecated: Canviat a estructura Visitable/Visitor


    """

    def __init__(self,ts):
        self._ts = ts


    def save_pickle(self,fname):
        with open(fname,'w') as f:
            pickle.dump(self._ts,f)
            f.close()

    def load_pickle(self,fname):
        """
        >>> from timeseries import TimeSeries
        >>> from measure import Measure
        >>> s = TimeSeries([Measure(1,2), Measure(3,4)])
        >>> ts = TimeSeriesStorage(s)
        >>> f = _doctest_file()
        >>> ts.save_pickle(f)
        >>> ns = ts.load_pickle(f)
        >>> s == ns
        True
        >>> _doctest_file_rm(f)
        True
        """
        with open(fname,'r') as f:
            ts = pickle.load(f)
            f.close()

        return ts

    
    def save_csv(self,fname):
        with open(fname,'w') as f:
            csvwriter = csv.writer(f)
            for m in self._ts:
                if isinstance(m.v, list):
                    cv = [m.t] + m.v
                else:
                    cv = [m.t,m.v]
                csvwriter.writerow(cv)
            f.close()

    def load_csv(self,fname,ttype=None,vtype=None,mtype=Measure):
        """
        Recuperador a partir d'un fitxer en format CSV. En el fittxer
        els valors desats són strings, en cas que es vulgui
        convertir-los cal indicar el tipus amb `ttype` i `vtype`.

        :type fname: str
        :type ttype: type
        :type vtype: type
        :type mtype: type(Measure)

        >>> from timeseries import TimeSeries
        >>> from measure import Measure
        >>> s = TimeSeries([Measure(1,2), Measure(3,4)])
        >>> ts = TimeSeriesStorage(s)
        >>> f = _doctest_file()
        >>> ts.save_csv(f)
        >>> ns = ts.load_csv(f,int,int)
        >>> s == ns
        True
        >>> _doctest_file_rm(f)
        True
        >>> 
        >>> s = TimeSeries([Measure(1,[2,3]), Measure(3,[4,5])])
        >>> ts = TimeSeriesStorage(s)
        >>> f = _doctest_file()
        >>> ts.save_csv(f)
        >>> def strlist2int(l): return [int(e) for e in l]
        >>> ns = ts.load_csv(f,int,strlist2int)
        >>> s == ns
        True
        >>> _doctest_file_rm(f)
        True
        """
        ts = self._ts.empty()
        with open(fname,'r') as f:
            csvreader = csv.reader(f)

            for row in csvreader:
                if len(row) == 2:
                    t,v = row
                else:
                    t = row[0]
                    v = row[1:]
                    
                if ttype is not None:
                    t = ttype(t)
                if vtype is not None:
                    v = vtype(v)
                ts.add(mtype(t,v))     
               

            f.close()

        return ts




def _doctest_file(fname='TimeSeriesStorageDocTest.testing'):
    import os
    if os.path.exists(fname):
        print 'DOCTEST FILE EXISTS!!! MUST BE DELETED'
        return None
    return fname

def _doctest_file_rm(fname):
    import os
    if os.path.exists(fname):
        os.remove(fname)
        return True
