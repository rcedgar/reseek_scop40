#!/bin/bash -e

mkdir -p ../reseek_search
cd ../reseek_search

for mode in veryfast fast sensitive verysensitive
do
	/bin/time -v -o $mode.time \
		../bin/reseek \
		  -scop40bench ../reseek_db/scop40_family.cal \
		  -$mode \
		  -output $mode.tsv \
		  -epqx $mode.epq.tsv \
		  -benchmode ignore \
		  -log $mode.bench.log
done
