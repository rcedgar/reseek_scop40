#!/bin/bash -e

mkdir -p ../results

for level in sf fold
do
	./sensitivity_vs_error.py $level \
	  > ../results/sens_vs_err_$level.tsv
	ls -lh ../results/sens_vs_err_$level.tsv
done
