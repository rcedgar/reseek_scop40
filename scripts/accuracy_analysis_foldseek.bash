#!/bin/bash -e

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

for mode in ignore family fold
do
	out=foldseek_$mode.txt
	if [ ! -s $out ] ; then
		sort -gk11 ../foldseek_search/foldseek.tsv \
		  | python3 ../scripts/accuracy_analysis.py 1 2 11 e $mode \
		  > foldseek_$mode.txt
	ls -lh foldeek_$mode.txt
	fi
done
