#!/usr/bin/python3

import sys
import math

fns = sys.argv[1:]

def getline():
    global f, line
    line = f.readline()
    assert len(line) > 0

'''
    0                         1     2               3      4     5     6         7           8       9
    1 ../scop40pdb/pdb//d12asa_ Chn:A          1.0000 1.0000  0.00   327     1-327       1-327     327
    2 ../scop40pdb/pdb//d1nnha_ Chn:A          0.8309 0.7510  2.75   275     1-327       9-293     293
    3 ../scop40pdb/pdb//d1rzhh2 Chn:H          0.7574 0.0759  0.59    25   126-150       1-25       25
'''

hits = 0
def dofile(fn):
    global f, line, hits
    f = open(fn)
    while 1:
        getline()
        if line.startswith(" Query"):
            break
    getline()
    query = line.split("//")[1]
    query = query.split()[0]
    while 1:
        getline()
        if line.startswith("   No.|"):
            break
    getline()
    while 1:
        getline()
        if line.find("../scop40pdb/pdb//") < 0:
            break
        hits += 1
        flds = line.split()
        target = flds[1].replace("../scop40pdb/pdb//", "")
        if query == target:
            continue
        tm1 = float(flds[3])
        tm2 = float(flds[4])
        geomean = math.sqrt(tm1*tm2)
        print("%s\t%s\t%.4f" % (query, target, geomean))

n = 0    
for fn in fns:
    n += 1
    if n%100 == 0:
        sys.stderr.write("%d\r", n)
    dofile(fn)
sys.stderr.write("%d\n", n)

nrq = len(fns)
sys.stderr.write("%u queries, %.1f hits/query\n" % (nrq, hits/nrq))
