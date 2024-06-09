#!/bin/bash -e

mkdir -p ../devreseek_search
cd ../devreseek_search

for mode in veryfast fast sensitive
do
	/bin/time -v -o dev$mode.time \
		$src/reseek/bin/reseek \
		  -search ../reseek_db/scop40.cal \
		  -evalue 99999 \
		  -$mode \
		  -output dev$mode.tsv \
		  -log dev$mode.search.log
done
