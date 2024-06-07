#!/bin/bash -e

./download_alns.bash

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

for mode in ignore sf fold
do
	out=TMalign_$mode.txt
	if [ ! -s $out ] ; then
		sort -rgk3 ../alns/TMalign.txt \
		  | python3 ../scripts/accuracy_analysis.py 1 2 3 s $mode \
		  > $out
	fi
	ls -lh $out
done
