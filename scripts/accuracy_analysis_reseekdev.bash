#!/bin/bash -e

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

for algo in veryfast fast sensitive verysensitive
do
	for mode in ignore family fold
	do
		out=devreseek-${algo}_$mode.txt
		if [ ! -s $out ] ; then
			sort -gk1 ../reseek_search/dev$algo.tsv \
			  | python3 ../scripts/accuracy_analysis.py 2 3 1 e $mode \
			  > $out
		fi
		ls -lh $out
	done
done
