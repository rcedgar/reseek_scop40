#!/bin/bash -e

mkdir -p ../reseek_search
cd ../reseek_search

for mode in veryfast fast sensitive verysensitive
do
	/bin/time -v -o $mode.time \
		../bin/reseekdev \
		  -search ../reseek_db/scop40.cal \
		  -$mode \
		  -output dev$mode.tsv \
		  -log dev$mode.search.log
done
