#!/usr/bin/python

import re
import subprocess

def executa(ordre):
    """
    :param str ordre: comanda que es vol executar amb els params i opcions
    :return: una llista de les linies de sortida per stdout de la comanda
    :rtype: list
    """
    p = subprocess.Popen(ordre, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    #for line in p.stdout.readlines():
    #    print line,
    retval = p.wait()
    return p.stdout.read().splitlines()

    

#----- main -----


RRD = 'itic.rrd'
COL = 'http_res'
DESTI = 'velocitat.rrd'


info = executa('rrdtool info {0}'.format(RRD))
max_rra = 0
#cerca max_rra
for i in info:
    i = i.strip()
    if i.startswith('rra'):
        #rra[14]
        index_rra = re.findall('rra\[(\d+)\]',i)[0]
        max_rra = max(max_rra,index_rra)

last = int( executa('rrdtool last {0}'.format(RRD))[0] )
first = int( executa('rrdtool first {0} --rraindex {1}'.format(RRD,max_rra))[0] )


min_step = ''
start = last
taules = []

while start > first:
    #exporta amb step mes petit
    ordre = 'rrdtool xport --end {2} --maxrows 2000 --step 1 DEF:xx={0}:{1}:AVERAGE XPORT:xx:"{1}"'.format(RRD,COL,start)
    export=executa(ordre)
    
    #cerca 'start' i les dades
    llegint_dades = False
    for v in export:
        if '</data>' in v:
            llegint_dades = False
            taules = [(step,valors)] + taules

        if llegint_dades:
            #<row><t>1298715000</t><v>1.3541712000e-01</v></row>
            s = v.strip()
            it=s.find('<t>')
            ft=s.find('</t>')
            temps = int( re.findall('<t>(\d+)</t>',s)[0] )
            iv=s.find('<v>')
            fv=s.find('</v>')
            valors.append( ( temps , s[iv+3:fv] ) )

        if '<data>' in v:
            #llegeix data
            llegint_dades = True
            valors = []

        
        if '<start>' in v:
            start = int( re.findall('\d+',v.strip())[0] )

        if '<step>' in v:
            step = int( re.findall('\d+',v.strip())[0] )
            min_step = min(min_step,step)

 



#---------- recupera ------------

step0,val0 = taules[0]
t0,v0 = val0[0]


temps = t0
for rra in taules:
    step,valors = rra
    print "Actualitzant RRA {0}".format(step)
    for val in valors:
        t,v = val
        
        while temps <= t:
            #actualitza amb el valor v tants intervals com faci falta per complir amb ekl minim step
            if v <> 'NaN':
                #no cal posar-hi els NaN, ja ho fara RRDtool 
                executa('rrdtool update {0} {1}:{2}'.format(DESTI,temps,v))
            temps += min_step
        

