
import sys
import csv
import time, datetime


def datetimetotimestamp(t):  
    return float(time.mktime(t.timetuple()))

def calendar2timestamp(t):
    t1 = datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    return datetimetotimestamp(t1)


def processa(fitxer,resultat):

    f = csv.reader(open(fitxer))
    fr = open(resultat,'w')

    
    inici = """
BEGIN;
VAR dadesoriginals BASE SAME_TYPE_AS ( timeseries) KEY { t };

dadesoriginals :=
RELATION {
    """
    final = """
};
    
END;
    """

    fr.write(inici)

    #primer
    rowprimer = 'TUPLE {{ t {0}, v {1} }}'
    t,v = f.next()
    fr.write(rowprimer.format(calendar2timestamp(t),v))

    #altres
    row = ',\nTUPLE {{ t {0}, v {1} }}' #AL DARRER NO HI pot anar coma 
    for t,v in f:      
        fr.write(row.format(calendar2timestamp(t),v))


    fr.write(final)
    fr.close()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        forig = sys.argv[1]
        fresult =  sys.argv[2]
        processa(forig,fresult)
    else:
        print 'usage: csc2rel.py orig.csv dest.d'
