import os
import csv
import datetime



def todatetime(fname):
    
    dates = {}
    with open(fname,'r') as f:
        r = csv.reader(f)
        for line in r:
            t,v = line
            t = datetime.datetime.fromtimestamp(float(t))
            dates[t] = v

    return dates

def modifica(fname,dates):

    with open(fname,'w') as f:
        r = csv.writer(f)
        for row in sorted(dates):
            r.writerow( (row,dates[row]) ) 




for fname in os.listdir('.'):
    if fname.endswith('.csv'):
        d = todatetime(fname)
        modifica(fname,d)
