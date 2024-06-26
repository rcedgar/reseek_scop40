#!/bin/bash -e

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

for mode in sf fold
do
	out=blastp_$mode.txt
	sort -gk11 ../blastp_search/blastp.tsv \
	  | python3 ../scripts/accuracy_analysis.py 1 2 11 e $mode \
	  > $out
	ls -lh $out
done
