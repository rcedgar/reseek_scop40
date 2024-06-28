#!/bin/bash -e

mkdir -p ../devreseek_search
cd ../devreseek_search

/bin/time -v -o devreseek.time \
	$src/reseek/bin/reseek \
	  -search ../reseek_db/scop40.cal \
	  -output devreseek.tsv \
	  -log devreseek.search.log
