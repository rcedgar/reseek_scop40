#!/bin/bash -e

mkdir -p ../reseek_search
cd ../reseek_search

for mode in veryfast fast sensitive
do
	/bin/time -v -o $mode.time \
		../bin/reseek \
		  -search ../reseek_db/scop40.cal \
		  -$mode \
		  -output $mode.tsv \
		  -log $mode.search.log
done

mode=verysensitive
/bin/time -v -o $mode.time \
	../bin/reseek \
	  -search ../reseek_db/scop40.cal \
	  -verysensitive \
	  -evalue 99999 \
	  -output $mode.tsv \
	  -log $mode.search.log
