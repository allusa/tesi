Fitxers mat
-----------

Fitxers binaris en format Matlab


Estructura::
 
 [ [[ ([[array([[ ([[296.75362799999999], [296.67306200000002], [296.59249599999998], [296.51193000000001],



Són ndarray http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html



Per llegir-los des de Python::

 >>> import scipy.io
 >>> x = scipy.io.loadmat('dades.mat',struct_as_record=True)

 >>> type(x)
 <type 'dict'>
 >>> x.keys()

 >>> s = x['sensors']
 >>> type(s)
 <type 'numpy.ndarray'>

 >>> v1 = s[0]
 >>> type(v1)
 <type 'numpy.ndarray'>

 >>> ftx = open('dad.txt','w')
 >>> ftx.write(str(v1))
 >>> ftx.close()

 >>> buit = v1[0][0][0]
 >>> type(buit)
 <type 'numpy.void'>

 >>> buit2 = buit[0][0][0][0][0]
 >>> type(buit2)
 <type 'numpy.void'>

 >>> buit2[0]
 array([[ 296.753628],
       [ 296.673062],
       [ 296.592496],
       ..., 
       [ 291.919668],
       [ 292.000234],
       [ 292.0808  ]])
 >>> buit2[0].ndim
 2
 >>> buit2[0][0]
 array([ 296.753628])
 >>> buit2[0][0][0]
 296.75362799999999

 >>> buit2[1]
 array([u'2010-04-29 12:05:07           ',
       u'2010-04-29 12:25:44           ',
       u'2010-04-29 12:27:51           ', ...,
       u'2011-10-18 13:22:09           ',
       u'2011-10-18 13:25:03           ', u'2011-10-18 13:27:59           '], 
      dtype='<U30')

 >>> buit2[1][0]
 u'2010-04-29 12:05:07           '






