# -*- encoding: utf-8 -*-

"""
=======
Storage
=======

:Abstract: Vegeu document principal `roundrobinson.py`
:Copyright: GPLv3


Implementació d'operacions d'emmagatzematge al disc per a les sèries temporals multiresolució
"""


import pickle
import csv
import os


class MultiresolutionStorage(object):
    """
    Objecte que agrupa les operacions d'emmagatzematge al disc en diferents formats:

    * pickle
    * csv


    """

    def __init__(self,mts):
        self._mts = mts


    def save_pickle(self,fname):
        with open(fname,'w') as f:
            pickle.dump(self._mts,f)
            f.close()

    def load_pickle(self,fname):
        """
        >>> m = _doctest_mrd()
        >>> ms = MultiresolutionStorage(m)
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

    
    def save_csv(self,dname):
        """
        Write a mrd values into a filesystem. Directory `dname` must be created.

        Sobre un load_csv: NO ES POSSIBLE RECUPERAR SI NO TENIM ELS AGREGADORS, guardem els buffers, k, etc.

        :param dname: Directory name
        :type dname: string

        >>> m = _doctest_mrd()
        >>> ms = MultiresolutionStorage(m)
        >>> d = _doctest_dir()
        >>> ms.save_csv(d)
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
            fname='R{delta}{f}.csv'.format(delta=r.B.delta,f=r.B.f.__name__)
            fpath = os.path.join(dname,fname)
            tss = r.D.s.storage().save_csv(fpath)



            



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
