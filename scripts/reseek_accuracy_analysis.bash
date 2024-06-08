#!/bin/bash -e

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

for algo in fast sensitive
do
	for mode in sf fold
	do
		out=reseek-${algo}_$mode.txt
		sort -gk1 ../reseek_search/$algo.tsv \
		  | python3 ../scripts/accuracy_analysis.py 2 3 1 e $mode \
		  > $out
		ls -lh $out
	done
done
