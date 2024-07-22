#!/bin/bash -e

./download_alns.bash

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

for mode in sf fold
do
	out=GTalign_$mode.txt
	sort -rgk3 ../gtalign_output/gtalign.tsv \
	  | python3 ../scripts/accuracy_analysis.py 1 2 3 s $mode \
	  > $out
	ls -lh $out
done
