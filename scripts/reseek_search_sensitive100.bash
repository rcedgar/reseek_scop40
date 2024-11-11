#!/bin/bash -e

mkdir -p ../reseek_search
cd ../reseek_search

/bin/time -v -o sensitive.time \
	reseek \
	  -search ../reseek_db/scop40.cal \
	  -output sensitive100.tsv \
	  -sensitive \
	  -evalue 100 \
	  -log sensitive100.search.log
