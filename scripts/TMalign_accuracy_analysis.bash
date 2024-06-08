#!/bin/bash -e

./download_alns.bash

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

for mode in sf fold
do
	out=TMalign_$mode.txt
	sort -rgk3 ../alns/TMalign.txt \
	  | python3 ../scripts/accuracy_analysis.py 1 2 3 s $mode \
	  > $out
	ls -lh $out
done
