#!/usr/bin/python3

import sys

minfpepq = 0.01
maxfpepq = 10
step = 0.1

fns = sys.argv[1:]

'''
NrDoms=11211 # number of domains
NrSingletons=2236 # number of singleton domains
NT=108718 # total possible TPs
NF=125566592 # total possible FPs
TPR+FPEPQ       0.0100  0.04513 38.7
TPR+FPEPQ       0.0200  0.1025  34.4
TPR+FPEPQ       0.0300  0.1655  32.3
TPR+FPEPQ       0.0400  0.2258  30.6
TPR+FPEPQ       0.0500  0.2915  29
'''

def dofile(fn):
    fpepqs = []
    for k in range(0, 101):
        fpepqs.append(None) 
    for line in open(fn):
        if not line.startswith("TPR+FPEPQ"):
            continue
        flds = line[:-1].split()
        assert len(flds) == 4
        assert flds[0] == "TPR+FPEPQ"
        sfpepq = flds[1]
        assert sfpepq[1] == '.'
        k = int(sfpepq[2] + sfpepq[3])
        if k >= 1 and k <= 100:
            fpepq = float(flds[2])
            fpepqs[k] = fpepq
    return fpepqs

name2fpepqs = {}
for fn in fns:
    fpepqs = dofile(fn)
    name = fn.replace(".txt", "")
    name2fpepqs[name] = fpepqs

names = list(name2fpepqs.keys())
hdrline = "fpepq"
for name in names:
    hdrline += "\t" + name
print(hdrline)

for k in range(1, 101):
    fpepq = k*0.01
    line = "%.2f" % fpepq
    for name in names:
        fpepqs = name2fpepqs[name]
        fpepq = fpepqs[k]
        if fpepq is None or fpepq < minfpepq or fpepq > maxfpepq:
            line += "\t"
        else:
            line += "\t%.4g" % fpepq
    print(line)

