#!/bin/bash -e

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

for mode in ignore family fold
do
	out=blastp_$mode.txt
	if [ ! -s $out ] ; then
		sort -gk11 ../blastp_search/blastp.tsv \
		  | python3 ../scripts/accuracy_analysis.py 1 2 11 e $mode \
		  > blastp_$mode.txt
	ls -lh blastp_$mode.txt
	fi
done
