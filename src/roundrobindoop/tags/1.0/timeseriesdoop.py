# -*- encoding: utf-8 -*-

"""
=====================
Sèrie temporal Hadoop
=====================

:Abstract: Vegeu document principal `roundrobindoop.py`
:Copyright: GPLv3

Implementació de les sèries temporals multiresolució en un Hadoop.
"""


import os
import glob
import subprocess
import datetime
import pickle
import marshal

from roundrobinson import MultiresolutionSeries, TimeSeries, Measure
from roundrobinson.storage import MultiresolutionStorage





class TsDoop(object):
    """
    >>> s = TimeSeries([Measure(1,2),Measure(2,1),Measure(6,3)])
    >>> m = MultiresolutionSeries()
    >>> m.addResolution(5,2,'mean') 
    >>> m.addResolution(10,4,'mean')
    >>>
    >>> sdoop = TsDoop(s,m)
    """

    rrdoop = 'rrdoop.py'

    def __init__(self,s,schema,debug=False):

        self._debug = debug

        self._s = s
        self._mts = schema

        self._name = 'roundrobindoop-ts-{0}'.format(datetime.datetime.now().strftime('%s'))
 

    def name_original(self):
        return '{0}.csv'.format(self._name)
    def name_schema(self):
        return '{0}.pickle'.format(self._name)
    def name_output(self):
        return '{0}-output.csv'.format(self._name)

    def path_rrdoop(self):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        return os.path.join(dir_path,self.rrdoop)

    def save_schema_pickle(self):
        schema = self.name_schema()
        if os.path.exists(schema):
            raise Exception('File {0} already exists'.format(schema))
        self._mts.storage().save_plain_pickle(schema)

    def save_ts(self):
        original = self.name_original()     
        if os.path.exists(original):
            raise Exception('File {0} already exists'.format(original))

        if isinstance(self._s,str):
            #is directly a file
            if not os.path.exists(self._s):
                raise Exception('File {0} directly declared but do not exists'.format(self._s))     
            os.symlink(self._s,original)
        else:
            self._s.storage().save_csv(original)


    def _parse_output_line(self,l):
        """
        >>> t = TsDoop(None,None)
        >>> t._parse_output_line("10/mean\\t10 2.0")
        (10, 'mean', 10, 2.0)
        >>> t._parse_output_line("10/mean\\t10 2.0 3.0 4.0")  
        (10, 'mean', 10, [2.0, 3.0, 4.0])
        """
        disc,ts = l.split('\t')
        delta,f = disc.split('/')
        tsplit = ts.split()
        t = int(tsplit[0])
        v = [ float(e) for e in tsplit[1:] ]
        if len(v) == 1:
            v = v[0]

        return (int(delta),f,t,v)


    def load_output(self):
        """
        Output té el format::

            10/mean	10 2.0
            5/mean	10 3.0
            5/mean	5 1.5

         o el multivaluat::

            300/mitjana     1409120400 2.08 0.0 9.83 0.0 0.76 0.9 8.19 2.16 15.52 nan nan nan nan nan nan nan nan nan
300/mitjana     1409120700 2.08 nan 9.83 nan 0.76 nan 8.28 2.52 15.7 nan nan nan nan nan nan nan nan nan
        """
        output = self.name_output()     
        mts = self._mts.empty()

        with open(output,'r') as o:
            for l in o:
                delta,f,t,v = self._parse_output_line(l)

                for r in mts:
                    if r.delta() == delta and r.fname() == f:
                        r.sd().add(Measure(t,v))

            o.close()     
        return mts



    def rm_temporals(self):
        original = self.name_original()
        schema = self.name_schema()
        output = self.name_output() 
        
        if os.path.exists(original):
            os.remove(original)
        if os.path.exists(schema):
            os.remove(schema)
        if os.path.exists(output):
            os.remove(output)



class TsDoopPipe(TsDoop):
    """
    rrdoop que s'executa amb pipes

    >>> s = TimeSeries([Measure(1,2),Measure(2,1),Measure(6,3)])
    >>> m = MultiresolutionSeries()
    >>> m.addResolution(5,2,'mean') 
    >>> m.addResolution(10,4,'mean')
    >>>
    >>> sdoop = TsDoopPipe(s,m)
    >>> nm = sdoop.execute()
    >>> r1,r2 = sorted(nm)
    >>> len(r1.sd())
    2
    >>> len(r2.sd())
    1
    """

    pipeorder = "cat {original} | {rrdoop} -map -schema {schema} | sort -k1,1 | {rrdoop} -reduce -schema {schema} >> {output}"


    def pipe_order(self):
        order = self.pipeorder.format(
            original=self.name_original(),
            schema = self.name_schema(),
            output = self.name_output(),
            rrdoop = self.path_rrdoop())

        return order


    def execute(self):

        self.save_schema_pickle()
        self.save_ts()
        
        order = self.pipe_order()

        r = subprocess.check_output(order,shell=True)
        if self._debug:
            print r

        mts = self.load_output()

        self.rm_temporals()

        return mts
        


class TimeSeriesDoop(object):
    """

    :param ddoop: Directory in dfs where time series will be stored 

    >>> s = TimeSeries([Measure(1,2),Measure(2,1),Measure(6,3)])
    >>> m = MultiresolutionSeries()
    >>> m.addResolution(5,2,'mean')
    >>> m.addResolution(10,4,'mean')
    >>>
    >>> sdoop = TimeSeriesDoop(s,m,'/user/aleix/')
    >>> #sdoop.save_schema_pickle('prova')
    >>> #sdoop.copytodfs()
    >>> #sdoop.execute_hadoop()
    >>> #sdoop.copydfsoutput()
    >>> #sdoop.load_mts_hadooped()
    >>> #sdoop.rm_temporals()
    """

    rrdoop = 'rrdoop.py'
    hadoop = '/usr/bin/hadoop'
    hadoop_streaming = '/usr/lib/hadoop/contrib/streaming/hadoop-streaming*.jar'

    def __init__(self,s,schema,ddoop,debug=False):

        self._debug = debug
        self.check_hadoop()

        self._s = s
        self._schema = schema

        self._name = 'roundrobindoop-ts-{0}'.format(datetime.datetime.now().strftime('%s'))
        self._ddoop = ddoop



    def check_hadoop(self):
        if not os.path.exists(self.hadoop):
            raise Exception('Hadoop path not found')

        if len(glob.glob(self.hadoop_streaming)) == 0:
            raise Exception('Hadoop streaming library not found')     

        r = subprocess.check_output([self.hadoop, 'version'])
        if self._debug:
            print r


    def name_original(self):
        return '{0}.csv'.format(self._name)

    def name_schema(self):
        return '{0}.pickle'.format(self._name)

    def name_output(self):
        return '{0}-output.csv'.format(self._name)

    def path_doopstreaming(self):
        l = glob.glob(self.hadoop_streaming)
        if len(l) > 0:
            return l[0]

    def pathdoop_original(self):
        return os.path.join(self._ddoop,self.name_original())

    def pathdoop_output(self):
        return os.path.join(self._ddoop,self._name)



    def save_schema_pickle(self,fname):
        schema = [(r.delta,r.tau,r.f,r.k) for r in self._schema ]

        with open(fname,'w') as f:
            pickle.dump(schema,f)
            f.close()


    def copytodfs(self):
        original = self.name_original()
        schema = self.name_schema()
        
        if os.path.exists(original):
            raise Exception('File {0} already exists'.format(original))
        if os.path.exists(schema):
            raise Exception('File {0} already exists'.format(schema))
        
        self._s.storage().save_csv(original)
        self.save_schema_pickle(schema)


        pathdoop = self.pathdoop_original()
        r = subprocess.check_output([self.hadoop,'dfs','-copyFromLocal',original,pathdoop])
        if self._debug:
            print r


    def copydfsoutput(self):

        doopoutput = self.pathdoop_output() + '/part-00000'
        output = self.name_output() 

        r = subprocess.check_output([self.hadoop,'dfs','-copyToLocal',doopoutput,output])
        if self._debug:
            print r

            


    def rm_temporals(self):
        original = self.name_original()
        schema = self.name_schema()
        output = self.name_output() 
        
        if os.path.exists(original):
            os.remove(original)
        if os.path.exists(schema):
            os.remove(schema)
        if os.path.exists(output):
            os.remove(output)

        dooporiginal = self.pathdoop_original()
        r = subprocess.check_output([self.hadoop,'dfs','-rm',dooporiginal])
        if self._debug:
            print r

        doopoutput = self.pathdoop_output()
        r = subprocess.check_output([self.hadoop,'dfs','-rmr',doopoutput])
        if self._debug:
            print r


    def execute_hadoop(self):
        dooporiginal = self.pathdoop_original()
        doopoutput = self.pathdoop_output()
        doopstreaming = self.path_doopstreaming()
        schema = self.name_schema()


 
        maper = '"{0} -map -schema {1}"'.format(self.rrdoop,schema)
        reducer = '"{0} -reduce -schema {1}"'.format(self.rrdoop,schema)
 
        r = subprocess.check_output([self.hadoop,'jar',doopstreaming,
                               '-file',self.rrdoop,
                               '-file',schema,
                               '-mapper', maper,
                               '-reducer',reducer,
                               '-input',dooporiginal,
                               '-output',doopoutput])

        if self._debug:
            print r



    def load_mts_hadooped(self,fname):

        mts = MultiresolutionSeries() #hauria de tenir l'equema self._schema

        with open(fname,'r') as f:

            for line in f:
                line = line.rstrip()
                res,tv = line.split('\t')
                d,f = res.split('/')
                t,v = tv.split()

                d = int(d)
                t = int(t)
                v = float(v)

                r = mts.getResolutionByName(d,f)
                r.s.add(t,v)

            f.close()
