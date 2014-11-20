import os, sys
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


def conv(fname):
    d = todatetime(fname)
    modifica(fname,d)

            
def default():

    for fname in os.listdir('.'):
        if fname.endswith('.csv'):
            conv(fname)

if __name__ == '__main__':

    if len(sys.argv) == 2:
        f = sys.argv[1]
        conv(f)
    else:
        default()
