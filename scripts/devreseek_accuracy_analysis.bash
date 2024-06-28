#!/bin/bash -e

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

for mode in sf fold
do
	out=devreseek_$mode.txt
	sort -gk1 ../devreseek_search/devreseek.tsv \
	  | python3 ../scripts/accuracy_analysis.py 2 3 1 e $mode \
	  > $out
	ls -lh $out
done
