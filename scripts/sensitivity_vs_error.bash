#!/bin/bash -e

mkdir -p ../sensitivity_vs_error
cd ../accuracy_analysis

for mode in family sf fold
do
	../scripts/sensitivity_vs_error_rate.py `ls *_$mode.txt | grep -v veryfast` \
	  > ../sensitivity_vs_error/$mode.tsv
	ls -lh ../sensitivity_vs_error/$mode.tsv
done
