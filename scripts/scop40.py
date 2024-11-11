# scop40 library functions

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

class Scop40:
	def score1_is_better(self, score1, score2):
		if self.se == 's':
			return score1 > score2
		elif self. se == 'e':
			return score1 < score2
		else:
			assert False

	def set_possible_tfs_sf(self):
		self.dom2nrpossibletps = {}
		self.NT = 0
		for dom in self.doms:
			sf = self.dom2sf[dom]
			sfsize = self.sf2size[sf]
			assert sfsize > 0
			if sfsize == 1:
				self.nrsingletons += 1
			self.dom2nrpossibletps[dom] = sfsize - 1
			self.NT += sfsize - 1
		self.NF = self.nrdompairs - self.NT # total possible FPs

	def set_possible_tfs_fold(self):
		self.dom2nrpossibletps = {}
		self.NT = 0
		for dom in self.doms:
			fold = self.dom2fold[dom]
			foldsize = self.fold2size[fold]
			assert foldsize > 0
			if foldsize == 1:
				self.nrsingletons += 1
			self.dom2nrpossibletps[dom] = foldsize - 1
			self.NT += foldsize - 1
		self.NF = self.nrdompairs - self.NT # total possible FPs

	def set_possible_tfs(self):
		self.nrdoms = len(self.doms)
		self.nrdompairs = self.nrdoms*self.nrdoms - self.nrdoms
		self.nrsingletons = 0 # nr singleton domains (no possible non-trivial TPs)

		if self.level == "sf":
			self.set_possible_tfs_sf()
		elif self.level == "fold":
			self.set_possible_tfs_fold()
		else:
			assert False

	def read_dom2scopid(self, dom2scopid_fn):
		self.doms = set()
		self.fams = set()
		self.sfs = set()
		self.folds = set()
		self.fam2doms = {}
		self.sf2doms = {}
		self.fold2doms = {}
		self.dom2fam = {}
		self.dom2sf = {}
		self.dom2fold = {}

		for line in open(dom2scopid_fn):
			flds = line[:-1].split('\t')
			assert len(flds) == 2
			dom = flds[0]
			scopid = flds[1]
			assert dom not in self.doms
			self.doms.add(dom)

			fam = scopid
			sf = getsf(scopid)
			fold = getfold(scopid)

			self.dom2fam[dom] = scopid
			self.dom2sf[dom] = sf
			self.dom2fold[dom] = fold

			if not fam in self.fams:
				self.fam2doms[fam] = []
				self.fams.add(fam)
			self.fam2doms[fam].append(dom)

			if not sf in self.sfs:
				self.sf2doms[sf] = []
				self.sfs.add(sf)
			self.sf2doms[sf].append(dom)

			if not fold in self.folds:
				self.fold2doms[fold] = []
				self.folds.add(fold)
			self.fold2doms[fold].append(dom)

		if self.level == "sf":
			self.sf2size = {}
			for sf in self.sfs:
				self.sf2size[sf] = len(self.sf2doms[sf])
		elif self.level == "fold":
			self.fold2size = {}
			for fold in self.folds:
				self.fold2size[fold] = len(self.fold2doms[fold])
		else:
			assert False

	def eval_unsorted(self, qs, ts, scores):
		nrhits = len(qs)
		assert nrhits > 10
		assert len(ts) == nrhits
		assert len(scores) == nrhits
		v = [ (scores[i], i) for i in range(nrhits) ]
		do_reverse = (self.se == "s")
		v_sorted = sorted(v, reverse=do_reverse)
		qs_sorted = []
		ts_sorted = []
		scores_sorted = []
		for _, i in v_sorted:
			qs_sorted.append(qs[i])
			ts_sorted.append(ts[i])
			scores_sorted.append(scores[i])
		self.eval_sorted(qs_sorted, ts_sorted, scores_sorted)

	# 0-based field nrs
	def eval_file(self, fn, qfldnr, tfldnr, scorefldnr, is_sorted):
		qs = []
		ts = []
		scores = []
		for line in open(fn):
			flds = line[:-1].split('\t')
			qs.append(flds[qfldnr])
			ts.append(flds[tfldnr])
			scores.append(float(flds[scorefldnr]))
		if is_sorted:
			self.eval_sorted(qs, ts, scores)
		else:
			self.eval_unsorted(qs, ts, scores)

	def eval_sorted(self, qs, ts, scores):
		nrhits = len(qs)
		assert nrhits > 10
		assert len(ts) == nrhits
		assert len(scores) == nrhits

		ntp = 0         # accumulated nr of TP hits
		nfp = 0         # accumulated nr of FP hits
		tpstep = 0.01   # bin size for TPs (X axis tick marks)
		tprt = 0.01     # TPR threshold, increases in steps of tpstep

		self.tpr_at_fpepq0_1 = None
		self.tpr_at_fpepq1 = None
		self.tpr_at_fpepq10 = None

		self.roc_tprs = []
		self.roc_epqs = []
		self.roc_scores = []

		dom2score_firstfp = {}
		for dom in self.doms:
			dom2score_firstfp[dom] = None

		tps = []
		for i in range(nrhits):
			q = qs[i].split('/')[0]
			t = ts[i].split('/')[0]
			score = scores[i]

			if i > 0 and last_score != score:
				if not self.score1_is_better(last_score, score):
					assert False, \
						f"Not sorted correctly {q=} {t=} {self.se=} {last_score=} {score=}"
			last_score = score

			if self.level == "sf":
				qsf = self.dom2sf[q]
				tsf = self.dom2sf[t]
				tp = (qsf == tsf)
			elif self.level == "fold":
				qfold = self.dom2fold[q]
				tfold = self.dom2fold[t]
				tp = (qfold == tfold)

			if tp:
				ntp += 1
			else:
				nfp += 1
				if dom2score_firstfp[q] is None or \
					self.score1_is_better(score, dom2score_firstfp[q]):
					dom2score_firstfp[q] = score
			tps.append(tp)

			# tpr=true-positive rate
			tpr = float(ntp)/self.NT

			# fpepq = false-positive errors per query
			fpepq = float(nfp)/self.nrdoms
			if fpepq >= 0.1 and self.tpr_at_fpepq0_1 is None:
				self.tpr_at_fpepq0_1 = tpr
			if fpepq >= 1 and self.tpr_at_fpepq1 is None:
				self.tpr_at_fpepq1 = tpr
			if fpepq >= 10 and self.tpr_at_fpepq10 is None:
				self.tpr_at_fpepq10 = tpr
			if tpr >= tprt:
				# print(f"TPR+FPEPQ\t%.4f\t%.4g\t%.4g" % (tprt, fpepq, score))
				self.roc_tprs.append(tprt)
				self.roc_epqs.append(fpepq)
				self.roc_scores.append(last_score)
				tprt += tpstep
			last_score = score

		if self.tpr_at_fpepq0_1 is None:
			self.tpr_at_fpepq0_1 = tpr

		if self.tpr_at_fpepq1 is None:
			self.tpr_at_fpepq1 = tpr

		if self.tpr_at_fpepq10 is None:
			self.tpr_at_fpepq1 = tpr
	
		nrhits = len(qs)
		assert len(tps) == nrhits

		tpr = float(ntp)/self.NT
		fpepq = float(nfp)/self.nrdoms
		# print(f"TPR+FPEPQ\t%.4f\t%.4g\t%.4g" % (tpr, fpepq, score))
		self.roc_tprs.append(tprt)
		self.roc_epqs.append(fpepq)
		self.roc_scores.append(last_score)

		self.nrtps_to_firstfp = 0
		for i in range(nrhits):
			score = scores[i]
			tp = tps[i]
			q = qs[i].split('/')[0]
			tp = tps[i]
			if tp and not dom2score_firstfp[q] is None and \
				self.score1_is_better(score, dom2score_firstfp[q]):
				self.nrtps_to_firstfp += 1
		self.sens_to_firstfp = float(self.nrtps_to_firstfp)/self.NT

	def __init__(self, se, level, dom2scopid_fn):
		assert se == "s" or se == "e" # score or E-value
		assert level == "sf" or level == "fold"

		self.se = se
		self.level = level
		if se == 's':
			self.low_score = -1
		elif se == 'e':
			self.low_score = 99999
		else:
			assert False

		self.read_dom2scopid(dom2scopid_fn)
		self.set_possible_tfs()

	def get_summary(self):
		summary = "SEPQ0.1=%.4f" % self.tpr_at_fpepq0_1
		summary += " SEPQ1=%.4f" % self.tpr_at_fpepq1
		summary += " SEPQ10=%.4f" % self.tpr_at_fpepq10
		summary += " S1FP=%.4f" % self.sens_to_firstfp
		summary += " N1FP=%u" % self.nrtps_to_firstfp
		return summary

	def roc2file(self, fn):
		n = len(self.roc_tprs)
		assert len(self.roc_epqs) == n
		assert len(self.roc_scores) == n
		f = open(fn, "w")
		f.write("tpr\tepq\tscore\n")
		for i in range(n):
			s = "%.4g" % self.roc_tprs[i]
			s += "\t%.4g" % self.roc_epqs[i]
			s += "\t%.4g" % self.roc_scores[i]
			f.write(s + '\n')
		f.close()
