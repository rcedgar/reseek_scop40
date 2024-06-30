#!/bin/bash -e

mkdir -p ../devreseek_search
cd ../devreseek_search

reseek=$src/reseek/bin/reseek

$reseek \
  -convert ../reseek_db/scop40.cal \
  -bca ../reseek_db/scop40.bca

/bin/time -v -o devreseek.time \
	$reseek \
	  -search ../reseek_db/scop40.bca \
	  -db ../reseek_db/scop40.bca \
	  -output devreseek.tsv \
	  -log devreseek.search.log

/bin/time -v -o devreseekfast.time \
	$reseek \
	  -search ../reseek_db/scop40.bca \
	  -db ../reseek_db/scop40.bca \
	  -fast \
	  -output devreseekfast.tsv \
	  -log devreseekfast.search.log
