#!/bin/bash -e

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

for algo in veryfast fast sensitive verysensitive
do
	for mode in ignore family fold
	do
		out=reseek-$algo.$mode.txt
		if [ ! -s $out ] ; then
			sort -gk1 ../reseek_search/$algo.tsv \
			  | python3 ../scripts/accuracy_analysis.py 2 3 1 e $mode \
			  > reseek-${algo}_$mode.txt
		fi
		ls -lh $out
	done
done
