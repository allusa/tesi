# -*- encoding: utf-8 -*-

"""
=======
Storage
=======

:Abstract: Vegeu document principal `pytsms.py`
:Copyright: GPLv3

Implementació d'operacions d'emmagatzematge al disc per a les sèries temporals
"""



import pickle
import csv

from measure import Measure


class SavePickle(object):
    """
    Un visitor
    """
    def __init__(fname):
        self.fname = fname

    def __call__(self,ob):
        with open(self.fname,'w') as f:
            pickle.dump(self._ts,f)
            f.close()
    


class TimeSeriesStorage(object):
    """
    Objecte que agrupa les operacions d'emmagatzematge al disc en diferents formats:

    * pickle
    * csv


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
