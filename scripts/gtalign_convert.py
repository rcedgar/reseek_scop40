#!/usr/bin/python3

import sys

infn = "../gtalign_output/gtalign-benchmark-data/gtalign_14_speed0_prescore03_addss_s044__scope20840__processed.out"

'''
2      d1914a2.ent  d2w9ja_.ent gtm1=  0.67465 gtm2=  0.77980 gbest= 0.779800  tm1=  0.67465 tm2=  0.77980 best= 0.779800
2      d16vpa_.ent  d1q90a3.ent gtm1=  0.11852 gtm2=  0.82743 gbest= 0.827430  tm1=  0.11875 tm2=  0.83357 best= 0.833570
2      d1a79a2.ent  d1r11a3.ent gtm1=  0.69019 gtm2=  0.84767 gbest= 0.847670  tm1=  0.69030 tm2=  0.84798 best= 0.847980
'''
for line in open(infn):
    flds = line[:-1].split()
    dom1 = flds[1].split('.')[0]
    dom2 = flds[2].split('.')[0]
    tm1 = float(flds[4])
    tm2 = float(flds[6])
    s = dom1
    s += "\t" + dom2
    s += "\t%.4f" % tm1
    print(s)

    s = dom2
    s += "\t" + dom1
    s += "\t%.4f" % tm2
    print(s)
