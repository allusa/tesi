# -*- encoding: utf-8 -*-

"""
=======
Storage
=======

:Abstract: Vegeu document principal `roundrobinson.py`
:Copyright: GPLv3


Implementació d'operacions d'emmagatzematge al disc per a les sèries temporals multiresolució


Les subclasses són visitors i, sigui `m=MultiresoltuionSeries()` es criden com:

* m.accept( Storage() )
* o bé Storage()(m)

Diferents formats:

* pickle
* plain.pickle
* csv



Els SavePickle i LoadPickle de pytsms ja són visitor per a les MultiresolutionSeries

    ALERTA!! que les funcions es guarden com a objectes en memòria
    i per tant no s'emmagatzemen i no es poden recuperar en altres
    sessions

>>> m = _doctest_mrd()
>>> f = _doctest_file()
>>> m.accept(SavePickle(f))
>>> nm = m.accept(LoadPickle(f))
>>> nm == m
True
>>> _doctest_file_rm(f)
True
"""

import os
import pickle, marshal, types
import csv


from pytsms.storage import SavePickle, LoadPickle, Storage, SaveCsv as TSSaveCsv




class SaveCsvDir(Storage):
    """
    Write a mrd values into a filesystem. Directory `dname` must be created.

    Sobre un LoadCsvDir: NO ES POSSIBLE RECUPERAR SI NO TENIM ELS AGREGADORS, guardem els buffers, k, etc.

    :param fname: Directory name
    :type fname: string

    >>> m = _doctest_mrd()
    >>> d = _doctest_dir()
    >>> m.accept(SaveCsvDir(d))
    >>> from pytsms import TimeSeries
    >>> from pytsms.storage import LoadCsv
    >>> s =  TimeSeries()
    >>> f1 = os.path.join(d,'R5mean.csv')
    >>> f2 = os.path.join(d,'R10mean.csv')
    >>> s1 = s.accept(LoadCsv(f1,int,float))
    >>> s2 = s.accept(LoadCsv(f2,int,float))
    >>> r1,r2 = sorted(m)
    >>> r1.D.s == s1
    True
    >>> r2.D.s == s2
    True
    >>> _doctest_dir_rm(d)
    True
    """
    def __call__(self,ob):
        dname = self.fname

        if not os.path.exists(dname):
            raise Exception('Directory {0} do not exist'.format(dname))
        
        
        for r in ob:
            fname='R{delta}{f}.csv'.format(delta=r.B.delta,f=r.fname())
            fpath = os.path.join(dname,fname)
            tss = r.D.s.accept(TSSaveCsv(fpath))




class SaveCsv(Storage):
    """
    Emmagatzema tot en un fitxer amb el format::

     #delta f t v
     10 mean 10 2.0
     5 mean 10 3.0
     5 mean 5 1.5

    >>> 
    """
    def __call__(self,on):    
        with open(fname,'w') as f:
            for r in sorted(ob):
                for m in r.sd():
                    s = '{delta} {fn} {t} {v}\n'.format(delta=r.delta(),fn=r.fname(),t=m.t,v=m.v)
                    f.write(s)
            f.close()




class MultiresolutionStorage(object):
    """
    Objecte que agrupa les operacions d'emmagatzematge al disc en diferents formats:

    * pickle
    * plain.pickle
    * csv

    :deprecated: Use Visitor Pattern

    """

    def __init__(self,mts):
        print "DEPRECATED: Use Visitor Pattern"
        self._mts = mts


    def save_pickle(self,fname):
        """
        ALERTA!! que les funcions es guarden com a objectes en memòria
        i per tant no s'emmagatzemen i no es poden recuperar en altres
        sessions
        """

        with open(fname,'w') as f:
            pickle.dump(self._mts,f)
            f.close()

    def load_pickle(self,fname):
        """
        >>> m = _doctest_mrd()
        >>> ms = MultiresolutionStorage(m)
        DEPRECATED: Use Visitor Pattern
        >>> f = _doctest_file()
        >>> ms.save_pickle(f)
        >>> nm = ms.load_pickle(f)
        >>> sorted(nm) == sorted(m) ##perque ordenat?
        True
        >>> _doctest_file_rm(f)
        True
        """
        with open(fname,'r') as f:
            mts = pickle.load(f)
            f.close()

        return mts


    def save_schema_plain_pickle(self,fname):
        """
        Pickle on només hi ha llistes, tuples i strings i per tant no depèn dels objectes
        """
        
        def _agg(r):
            if isinstance(r.f(),str):
                return r.fname()
            else:
                return (r.fname(),marshal.dumps(r.f().func_code))

        schema = [(r.delta(),r.tau(),_agg(r),r.k()) for r in self._mts ]

        with open(fname,'w') as f:
            pickle.dump(schema,f)
            f.close()


    def save_plain_pickle(self,fname):
        """
        Pickle on només hi ha llistes, tuples i strings i per tant no depèn dels objectes
        """
        raise NotImplemented('falta fer')



    def _despickle_f(self,f):
        name,content = f
        code = marshal.loads(content)
        func = types.FunctionType(code, globals(), name)
        return func


    def load_schema_plain_pickle(self,fname):
        """
        Pickle on només hi ha llistes, tuples i strings i per tant no depèn dels objectes

        >>> m = _doctest_mrd()
        >>> ms = MultiresolutionStorage(m)
        DEPRECATED: Use Visitor Pattern
        >>> f = _doctest_file()
        >>> ms.save_schema_plain_pickle(f)
        >>> nm = ms.load_schema_plain_pickle(f)
        >>> nm.schema_eq(m)
        True
        >>> _doctest_file_rm(f)
        True
        """
        from multiresolution import MultiresolutionSeries
        mts = MultiresolutionSeries()
        schema = self.load_pickle(fname)
        for r in schema:
            delta,tau,f,k = r
            f = self._despickle_f(f)
            mts.addResolution(delta,k,f,tau)
        return mts




    
    def save_dir_csv(self,dname):
        """
        Write a mrd values into a filesystem. Directory `dname` must be created.

        Sobre un load_dir_csv: NO ES POSSIBLE RECUPERAR SI NO TENIM ELS AGREGADORS, guardem els buffers, k, etc.

        :param dname: Directory name
        :type dname: string

        >>> m = _doctest_mrd()
        >>> ms = MultiresolutionStorage(m)
        DEPRECATED: Use Visitor Pattern
        >>> d = _doctest_dir()
        >>> ms.save_dir_csv(d)
        >>> from pytsms import TimeSeries
        >>> s =  TimeSeries()
        >>> f1 = os.path.join(d,'R5mean.csv')
        >>> f2 = os.path.join(d,'R10mean.csv')
        >>> s1 = s.storage().load_csv(f1,int,float)
        >>> s2 = s.storage().load_csv(f2,int,float)
        >>> r1,r2 = sorted(m)
        >>> r1.D.s == s1
        True
        >>> r2.D.s == s2
        True
        >>> _doctest_dir_rm(d)
        True
        """

        if not os.path.exists(dname):
            raise Exception('Directory {0} do not exist'.format(dname))
        
        
        for r in self._mts:
            fname='R{delta}{f}.csv'.format(delta=r.B.delta,f=r.fname())
            fpath = os.path.join(dname,fname)
            tss = r.D.s.storage().save_csv(fpath)



    def save_csv(self,fname):      
        """
        Emmagatzema tot en un fitxer amb el format::

         10/mean 10 2.0
         5/mean 10 3.0
         5/mean 5 1.5
        """
        pass

        





def _doctest_file(fname='MultiresolutionTimeSeriesStorageDocTest.testing'):
    if os.path.exists(fname):
        print 'DOCTEST FILE EXISTS!!! MUST BE DELETED'
        return None
    return fname

def _doctest_file_rm(fname):
    if os.path.exists(fname):
        os.remove(fname)
        return True

def _doctest_dir(dname='MultiresolutionTimeSeriesStorageDocTest.testing'):
    if os.path.exists(dname):
        print 'DOCTEST DIRECTORY EXISTS!!! MUST BE DELETED'
        return None
    os.mkdir(dname)
    return dname

def _doctest_dir_rm(dname):
    import shutil
    if os.path.exists(dname):
        shutil.rmtree(dname)
        return True


def _doctest_mrd():
    from pytsms import Measure, TimeSeries
    from multiresolution import MultiresolutionSeries
    from aggregators import mean

    m1 = Measure(1,10); m2 = Measure(5,10); m3 = Measure(10,40)
    M = MultiresolutionSeries()

    M.addResolution(5,2,mean)
    M.addResolution(10,4,mean)
    M.add(m1); M.add(m2); M.add(m3)
    M.consolidateTotal()
    return M
