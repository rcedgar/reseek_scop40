#!/bin/bash -e

mkdir -p ../reseek_search
cd ../reseek_search

for mode in veryfast fast sensitive
do
	/bin/time -v -o dev$mode.time \
		../bin/reseekdev \
		  -search ../reseek_db/scop40.cal \
		  -$mode \
		  -output dev$mode.tsv \
		  -log dev$mode.search.log
done

mode=verysensitive
/bin/time -v -o dev$mode.time \
	../bin/reseekdev \
	  -search ../reseek_db/scop40.cal \
	  -evalue 99999 \
	  -verysensitive \
	  -output dev$mode.tsv \
	  -log dev$mode.search.log
