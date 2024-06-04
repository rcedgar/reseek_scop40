#!/bin/bash -e

mkdir -p ../results
rm -f ../results/summary_*

./summary_table.py

for b in family fold ignore
do
	echo === $b ===
	./columnsl.py ../results/summary_table_$b.tsv \
	  | tee ../results/summary_table_$b.txt
done
