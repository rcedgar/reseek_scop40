#!/bin/bash -e

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

for mode in family sf fold
do
	out=foldseek_$mode.txt
	sort -gk11 ../foldseek_search/foldseek.tsv \
	  | python3 ../scripts/accuracy_analysis.py 1 2 11 e $mode \
	  > $out
	ls -lh $out
done
