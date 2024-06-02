#!/usr/bin/python3

# Extract subset from scop40pdb/alignResults/rawoutput
#  with family annotation in scop v1.17, convert to
#  tabbed text
#   1.  query_domain
#   2.  target_domain
#   3.  score/E-value
#	4.	T (same family) or F (different families)

import sys

algo = sys.argv[1]

dom2fam = {}
for line in open("../out/domain_family.tsv"):
	flds = line[:-1].split('\t')
	dom = flds[0]
	fam = flds[1]
	dom2fam[dom] = fam

sep = '\t'
if algo == "dali" or algo == "tm":
	sep = ' '

if algo.startswith("reseek"):
	aln = "/c/int/scop40pdb/reseek_output/" + algo + ".tsv"
else:
	aln = "/c/data/scop40pdb/alignResults/rawoutput/" + algo + "aln"

q_fieldnr = 0
t_fieldnr = 1
score_fieldnr = 2
if algo == "foldseek" or algo == "newfoldseek":
	score_fieldnr = 10
elif algo == "blastp":
	score_fieldnr = 10
elif algo.startswith("reseek"):
	score_fieldnr = 0
	q_fieldnr = 1
	t_fieldnr = 2

for line in open(aln):
	fields = line.split(sep)
	try:
		q = fields[q_fieldnr].split('/')[0]
		t = fields[t_fieldnr].split('/')[0]
		if q == t:
			continue
		qfam = dom2fam[q]
		tfam = dom2fam[t]
		score = fields[score_fieldnr].strip()
		if qfam == tfam:
			TF = 'T'
		else:
			TF = 'F'
	except:
		continue
	print(q + '/' + qfam + '\t' + t + '/' + tfam + '\t' + score + '\t' + TF)
