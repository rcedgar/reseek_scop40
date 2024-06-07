#!/usr/bin/python3

import sys
# from operator import itemgetter

qfldnr = int(sys.argv[1])
tfldnr = int(sys.argv[2])
scorefldnr = int(sys.argv[3])
se = sys.argv[4]
level = sys.argv[5]

assert se == "s" or se == "e" # score or E-value
assert level == "sf" or level == "fold" or level == "ignore"

if se == 's':
    low_score = -1
elif se == 'e':
    low_score = 99999
else:
    assert False
Doms = set()

# Scop identifier looks like a.1.2.3 
#     a    1           2      3
# class.fold.superfamily.family
def getfold(scopid):
    flds = scopid.split('.')
    assert len(flds) == 4
    fold = flds[0] + "." + flds[1]
    return fold

def getsf(scopid):
    flds = scopid.split('.')
    assert len(flds) == 4
    sf = flds[0] + "." + flds[1] + "." + flds[2]
    return sf

def score1_is_better(score1, score2):
    if se == 's':
        return score1 > score2
    elif se == 'e':
        return score1 < score2
    else:
        assert False

doms = set()
sfs = set()
folds = set()
sf2doms = {}
fold2doms = {}
dom2sf = {}
dom2fold = {}
for line in open("../data/scop_lookup.fix.tsv"):
    flds = line[:-1].split('\t')
    assert len(flds) == 2
    dom = flds[0]
    scopid = flds[1]
    assert dom not in doms
    doms.add(dom)

    sf = getsf(scopid)
    fold = getfold(scopid)

    dom2sf[dom] = sf
    dom2fold[dom] = fold

    if not sf in sfs:
        sf2doms[sf] = []
        sfs.add(sf)
    sf2doms[sf].append(dom)

    if not fold in folds:
        fold2doms[fold] = []
        folds.add(fold)
    fold2doms[fold].append(dom)

sf2size = {}
for sf in sfs:
    sf2size[sf] = len(sf2doms[sf])

fold2size = {}
for fold in folds:
    fold2size[fold] = len(fold2doms[fold])

# Possible nr TPs for a domain is all family members except self-hit
nrdoms = len(doms)

# Number of alignments minus trivial self-alignments
nrpairs = nrdoms*nrdoms - nrdoms

NT = 0 # total possible TPs
dom2nrpossibletps = {}

if level == "sf":
    nrsingletons = 0 # nr singleton domains (no possible non-trivial TPs)
    for dom in doms:
        sf = dom2sf[dom]
        sfsize = sf2size[sf]
        assert sfsize > 0
        if sfsize == 1:
            nrsingletons += 1
        dom2nrpossibletps[dom] = sfsize - 1
        NT += sfsize - 1
    NF = nrpairs - NT # total possible FPs

elif level == "fold":
    nrsingletons = 0 # nr singleton domains (no possible non-trivial TPs)
    for dom in doms:
        fold = dom2fold[dom]
        foldsize = fold2size[fold]
        assert foldsize > 0
        if foldsize == 1:
            nrsingletons += 1
        dom2nrpossibletps[dom] = foldsize - 1
        NT += foldsize - 1
    NF = nrpairs - NT # total possible FPs

elif level == "ignore":
    nrsingletons = 0 # nr singleton domains (no possible non-trivial TPs)
    NI = 0 # nr ignored pairs
    for dom in doms:
        n = 0
        sf = dom2sf[dom]
        fold = dom2fold[dom]
        fold_doms = fold2doms[fold]
        for fold_dom in fold_doms:
            if fold_dom == dom:
                continue
            fold_dom_sf = dom2sf[fold_dom]
            if fold_dom_sf == sf:
                n += 1
            else:
                NI += 1
        if n == 0:
            nrsingletons += 1
        dom2nrpossibletps[dom] = n
        NT += n
    NF = nrpairs - NT - NI # total possible FPs

dom2score_firstfp = {}
for dom in doms:
    dom2score_firstfp[dom] = low_score

print(f"{nrdoms=} # number of domains")
print(f"{nrsingletons=} # number of singleton domains")
print(f"{NT=} # total possible TPs")
print(f"{NF=} # total possible FPs")
if level == "ignore":
    print(f"{NI=} # number of ignored pairs")

scores = []
qs = []
ts = []
qdoms = []
tdoms = []
qfams = []
tfams = []
tps = []

ntp = 0 # accumulated nr of TP hits
nfp = 0 # accumulated nr of FP hits
last_score = None
tpstep = 0.01 # bin size for TPs (X axis tick marks)
tprt = 0.01 # TPR threshold, increases in steps of tpstep
tpr_at_fpepq0_1 = -1
tpr_at_fpepq1 = -1
tpr_at_fpepq10 = -1
prev_line = None
score = 0
for line in sys.stdin:
    fields = line[:-1].split('\t')
    q = fields[qfldnr-1]
    t = fields[tfldnr-1]
    # discard trivial self-hits, if present
    if q == t:
        continue
    
    score = float(fields[scorefldnr-1])

    if not last_score is None and last_score != score:
        if not score1_is_better(last_score, score):
            sys.stderr.write(f"\n\n{prev_line=}\n")
            sys.stderr.write(f"{line=}\n")
            sys.stderr.write(f"Not sorted correctly {se=} {last_score=} {score=}\n")
            assert False

    prev_line = line
    qdom = q
    tdom = t
    try:
        qsf = dom2sf[q]
        tsf = dom2sf[t]
    except:
        continue

    if level == "sf":
        tp = (qsf == tsf)
    elif level == "fold":
        qfold = dom2fold[qdom]
        tfold = dom2fold[tdom]
        tp = (qfold == tfold)
    elif level == "ignore":
        qfold = dom2fold[qdom]
        tfold = dom2fold[tdom]
        if qfold == tfold and qsf != tsf:
            continue
        tp = (qsf == tsf)

    qs.append(q)
    ts.append(t)

    scores.append(score)

    qdoms.append(qdom)
    tdoms.append(tdom)

    qfams.append(qsf)
    tfams.append(tsf)
    tps.append(tp)
    if tp:
        ntp += 1
    else:
        nfp += 1

    # tpr=true-positive rate
    tpr = float(ntp)/NT

    # fpepq = false-positive errors per query
    fpepq = float(nfp)/nrdoms
    if fpepq >= 0.1 and tpr_at_fpepq0_1 == -1:
        tpr_at_fpepq0_1 = tpr
    if fpepq >= 1 and tpr_at_fpepq1 == -1:
        tpr_at_fpepq1 = tpr
    if fpepq >= 10 and tpr_at_fpepq10 == -1:
        tpr_at_fpepq10 = tpr
    if tpr >= tprt:
        print(f"TPR+FPEPQ\t%.4f\t%.4g\t%.4g" % (tprt, fpepq, score))
        tprt += tpstep
    last_score = score

if tpr_at_fpepq0_1 == -1:
    tpr_at_fpepq0_1 = tpr

if tpr_at_fpepq1 == -1:
    tpr_at_fpepq1 = tpr

if tpr_at_fpepq10 == -1:
    tpr_at_fpepq10 = tpr
    
nrhits = len(qs)
assert len(tps) == nrhits

tpr = float(ntp)/NT
fpepq = float(nfp)/nrdoms
print(f"TPR+FPEPQ\t%.4f\t%.4g\t%.4g" % (tpr, fpepq, score))

for i in range(nrhits):
    score = scores[i]
    tp = tps[i]
    if not tp:
        qdom = qdoms[i]
        score = scores[i]
        if score1_is_better(score, dom2score_firstfp[qdom]):
            dom2score_firstfp[qdom] = score
nrtps_to_firstfp = 0
for i in range(nrhits):
    score = scores[i]
    tp = tps[i]
    qdom = qdoms[i]
    tp = tps[i]
    if tp and score1_is_better(score, dom2score_firstfp[qdom]):
        nrtps_to_firstfp += 1

# Foldseek paper definition of sensitivity
sens_to_firstfp = float(nrtps_to_firstfp)/NT

# print("tpr_at_fpepq0_1=%.4f" % tpr_at_fpepq0_1)
# print("tpr_at_fpepq1=%.4f" % tpr_at_fpepq1)
# print("tpr_at_fpepq10=%.4f" % tpr_at_fpepq10)
# print("nrtps_to_firstfp=%d" % nrtps_to_firstfp)
# print("sens_to_firstfp=%.4f" % sens_to_firstfp)

Summary = "SEPQ0.1=%.4f" % tpr_at_fpepq0_1
Summary += "\tSEPQ1=%.4f" % tpr_at_fpepq1
Summary += "\tSEPQ10=%.4f" % tpr_at_fpepq10
Summary += "\tS1FP=%.4f" % sens_to_firstfp
Summary += "\tlevel=%s" % level
print(Summary)
