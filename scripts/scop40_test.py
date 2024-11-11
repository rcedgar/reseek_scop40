#!/usr/bin/python3

import sys
from importlib.machinery import SourceFileLoader

scop40 = SourceFileLoader("scop40", "../scripts/scop40.py").load_module()

sc = scop40.Scop40("e", "sf", "../data/scop_lookup.fix.tsv")
sc.eval_file("../reseek_search/sensitive100.tsv", 1, 2, 0, False)
print(sc.get_summary())
sc.roc2file("roc.tmp")
