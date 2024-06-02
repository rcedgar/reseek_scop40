#!/bin/bash -e

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

for mode in veryfast fast sensitive verysensitive
do
	sort -gk1 ../reseek_search/dev$mode.tsv \
	  | python3 ../scripts/accuracy_analysis.py 2 3 1 e ignore \
	  > dev$mode.txt
done
