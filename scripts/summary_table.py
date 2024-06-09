#!/usr/bin/python3

import sys

algos = [ "TMalign", "blastp", "DALI", "foldseek" ]
algos += [ "devreseek-fast", "devreeek-sensitive" ]
bs = [ "sf", "fold" ]

'''
    Elapsed (wall clock) time (h:mm:ss or m:ss): 2:07.23
    Average shared text size (kbytes): 0
    Average unshared data size (kbytes): 0
    Average stack size (kbytes): 0
    Average total size (kbytes): 0
    Maximum resident set size (kbytes): 36804
'''
def get_secs_memmb(fn):
    secs = None
    memmb = None
    try:
        for line in open(fn):
            if line.find("Elapsed (wall clock) time") >= 0:
                s = line[:-1].split()[-1]
                s = s.split('.')[0]
                flds = s.split(':')
                assert len(flds) == 2
                secs = 60*int(flds[0]) + int(flds[1])
            elif line.find("Maximum resident set size (kbytes)") >= 0:
                memmb = int(line[:-1].split()[-1])//1024
    except:
        pass
    return secs, memmb

algo2sm = {}
algo2sm["blastp"] = get_secs_memmb("../blastp_search/blastp_search.time")
algo2sm["foldseek"] = get_secs_memmb("../foldseek_search/foldseek_search.time")

algo2sm["reseek-veryfast"] = get_secs_memmb("../reseek_search/veryfast.time")
algo2sm["reseek-fast"] = get_secs_memmb("../reseek_search/fast.time")
algo2sm["reseek-sensitive"] = get_secs_memmb("../reseek_search/sensitive.time")
algo2sm["reseek-verysensitive"] = get_secs_memmb("../reseek_search/verysensitive.time")

algo2sm["devreseek-veryfast"] = get_secs_memmb("../devreseek_search/devveryfast.time")
algo2sm["devreseek-fast"] = get_secs_memmb("../devreseek_search/devfast.time")
algo2sm["devreseek-sensitive"] = get_secs_memmb("../devreseek_search/devsensitive.time")
algo2sm["devreseek-verysensitive"] = get_secs_memmb("../devreseek_search/devverysensitive.time")
# print(algo2sm)
# print(algo2sm["reseek-sensitive"])

algob2dict = {}

def get_dict(algo, b):
    d = {}
    names = [ "tpr_at_fpepq0_1", "tpr_at_fpepq1", "tpr_at_fpepq10", "sens_to_firstfp" ]
    for name in names:
        d[name] = None
    fn = "../accuracy_analysis/" + algo + "_" + b + ".txt"
    for line in open(fn):
        flds = line[:-1].split("=")
        if len(flds) == 2 and flds[0] in names:
            d[flds[0]] = float(flds[1])
    return d

algo2tpr_at_fpepq0_1 = {}
for algo in algos:
    for b in bs:
        d = get_dict(algo, b)
        algo2tpr_at_fpepq0_1[algo] = d["tpr_at_fpepq0_1"]
        algob2dict[(algo, b)] = d

def get_value(x):
    return x[1]
algo2tpr_at_fpepq0_1_sorted = sorted(algo2tpr_at_fpepq0_1.items(), key=get_value)

def print_row(f, b, algo):
    try:
        secs, mb = algo2sm[algo]
    except:
        secs, mb = (None, None)
    tpr_at_fpepq0_1 = algob2dict[(algo, b)]["tpr_at_fpepq0_1"]
    tpr_at_fpepq1 = algob2dict[(algo, b)]["tpr_at_fpepq1"]
    tpr_at_fpepq10 = algob2dict[(algo, b)]["tpr_at_fpepq10"]
    sens_to_firstfp = algob2dict[(algo, b)]["sens_to_firstfp"]

    if tpr_at_fpepq0_1 is None or tpr_at_fpepq0_1 < 0:
        row = "-"
    else:
        row = "%.4f" % tpr_at_fpepq0_1

    if tpr_at_fpepq1 is None or tpr_at_fpepq1 < 0:
        row += "\t-"
    else:
        row += "\t%.4f" % tpr_at_fpepq1

    if tpr_at_fpepq10 is None or tpr_at_fpepq10 < 0:
        row += "\t-"
    else:
        row += "\t%.4f" % tpr_at_fpepq10

    if sens_to_firstfp is None or sens_to_firstfp < 0:
        row += "\t-"
    else:
        row += "\t%.4f" % sens_to_firstfp

    if secs is None:
        row += "\t-"
    else:
        row += "\t%d" % secs

    if secs is None:
        row += "\t-"
    else:
        row += "\t%.1f" % mb
    row += "\t" + algo
    f.write(row + "\n")

b2short = { "fold" : "fld", "family" : "fam" }
for b in bs:
    f = open("../results/summary_table_" + b + ".tsv", "w")
    f.write("Sens0.1_%s\tSens1_%s\tSens10_%s\tSens1FP_%s\tSecs\tMb\tMethod\n" \
            % (b, b, b, b))
    for algo, _ in list(algo2tpr_at_fpepq0_1_sorted):
        print_row(f, b, algo)
    f.close()
