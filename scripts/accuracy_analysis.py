#!/usr/bin/python3

import sys
from operator import itemgetter

qfldnr = int(sys.argv[1])
tfldnr = int(sys.argv[2])
scorefldnr = int(sys.argv[3])
se = sys.argv[4]
level = sys.argv[5]

assert se == "s" or se == "e" # score or E-value
assert level == "family" or level == "fold" or level == "ignore"

if se == 's':
	low_score = -1
elif se == 'e':
	low_score = 99999
else:
	assert False
Doms = set()

DomToFam = {}
for Line in open("../data/scop_lookup.tsv"):
    Fields = Line[:-1].split('\t')
    assert len(Fields) == 2
    Dom = Fields[0]
    Fam = Fields[1]
    Doms.add(Dom)
    DomToFam[Dom] = Fam

def score1_is_better(score1, score2):
	if se == 's':
		return score1 > score2
	elif se == 'e':
		return score1 < score2
	else:
		assert False

def getfold(fam):
	n = fam.rfind('.')
	return fam[:n]

doms = set()
fams = set()
folds = set()
fam2doms = {}
fold2doms = {}
dom2fam = {}
dom2fold = {}
for line in open("../data/scop_lookup.tsv"):
	flds = line[:-1].split('\t')
	dom = flds[0]
	fam = flds[1]
	fold = getfold(fam)
	assert dom not in doms
	doms.add(dom)
	if level == "fold":
		fam = getfold(fam)
	dom2fam[dom] = fam
	dom2fold[dom] = fold
	if not fam in fams:
		fam2doms[fam] = []
		fams.add(fam)
	if not fold in folds:
		fold2doms[fold] = []
		folds.add(fold)
	fam2doms[fam].append(dom)
	fold2doms[fold].append(dom)

fam2size = {}
for fam in fams:
	fam2size[fam] = len(fam2doms[fam])

fold2size = {}
for fold in folds:
	fold2size[fold] = len(fold2doms[fold])

# Possible nr TPs for a domain is all family members except self-hit
NrDoms = len(doms)

# Number of alignments minus trivial self-alignments
NrPairs = NrDoms*NrDoms - NrDoms

NT = 0 # total possible TPs
dom2nrpossibletps = {}

if level == "family":
	NrSingletons = 0 # nr singleton domains (no possible non-trivial TPs)
	for dom in doms:
		fam = dom2fam[dom]
		famsize = fam2size[fam]
		assert famsize > 0
		if famsize == 1:
			NrSingletons += 1
		dom2nrpossibletps[dom] = famsize - 1
		NT += famsize - 1
	NF = NrPairs - NT # total possible FPs

elif level == "fold":
	NrSingletons = 0 # nr singleton domains (no possible non-trivial TPs)
	for dom in doms:
		fold = dom2fold[dom]
		foldsize = fold2size[fold]
		assert foldsize > 0
		if foldsize == 1:
			NrSingletons += 1
		dom2nrpossibletps[dom] = foldsize - 1
		NT += foldsize - 1
	NF = NrPairs - NT # total possible FPs

elif level == "ignore":
	NrSingletons = 0 # nr singleton domains (no possible non-trivial TPs)
	NI = 0 # nr ignored pairs
	for dom in doms:
		n = 0
		fam = dom2fam[dom]
		fold = dom2fold[dom]
		fold_doms = fold2doms[fold]
		for fold_dom in fold_doms:
			if fold_dom == dom:
				continue
			fold_dom_fam = dom2fam[fold_dom]
			if fold_dom_fam == fam:
				n += 1
			else:
				NI += 1
		if n == 0:
			NrSingletons += 1
		dom2nrpossibletps[dom] = n
		NT += n
	NF = NrPairs - NT - NI # total possible FPs

dom2score_firstfp = {}
for dom in doms:
	dom2score_firstfp[dom] = low_score


print(f"{NrDoms=} # number of domains")
print(f"{NrSingletons=} # number of singleton domains")
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
		qfam = DomToFam[q]
		tfam = DomToFam[t]
	except:
		continue

	if level == "family":
		tp = (qfam == tfam)
	elif level == "fold":
		qfold = getfold(qfam)
		tfold = getfold(tfam)
		tp = (qfold == tfold)
	elif level == "ignore":
		qfold = getfold(qfam)
		tfold = getfold(tfam)
		if qfold == tfold and qfam != tfam:
			continue
		tp = (qfam == tfam)

	qs.append(q)
	ts.append(t)

	scores.append(score)

	qdoms.append(qdom)
	tdoms.append(tdom)

	qfams.append(qfam)
	tfams.append(tfam)
	tps.append(tp)
	if tp:
		ntp += 1
	else:
		nfp += 1

	# tpr=true-positive rate
	tpr = float(ntp)/NT

	# fpepq = false-positive errors per query
	fpepq = float(nfp)/NrDoms
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

nrhits = len(qs)
assert len(tps) == nrhits

tpr = float(ntp)/NT
fpepq = float(nfp)/NrDoms
print(f"TPR+FPEPQ\t%.4f\t%.4g\t%.4g" % (tpr, fpepq, score))
print("tpr_at_fpepq0_1=%.4f" % tpr_at_fpepq0_1)
print("tpr_at_fpepq1=%.4f" % tpr_at_fpepq1)
print("tpr_at_fpepq10=%.4f" % tpr_at_fpepq10)

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
print("nrtps_to_firstfp=%d" % nrtps_to_firstfp)
print("sens_to_firstfp=%.4f" % sens_to_firstfp)
