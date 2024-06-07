#!/bin/bash -e

./download_gtalign_output.bash

mkdir -p ../accuracy_analysis

./gtalign_convert.py > ../gtalign_output/hits.tsv

cd ../accuracy_analysis

for mode in ignore sf fold
do
	out=gtalign_$mode.txt
	if [ ! -s $out ] ; then
		sort -rgk3 ../gtalign_output/hits.tsv \
		  | python3 ../scripts/accuracy_analysis.py 1 2 3 s $mode \
		  > $out
	fi
	ls -lh $out
done
