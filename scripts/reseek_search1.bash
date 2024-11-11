#!/bin/bash -e

mkdir -p ../reseek_search
cd ../reseek_search

mode=default

/bin/time -v -o $mode.time \
	reseek \
	  -search ../reseek_db/scop40.cal \
	  -output $mode.tsv \
	  -log $mode.search.log
