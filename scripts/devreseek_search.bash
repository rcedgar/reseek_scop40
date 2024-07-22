#!/bin/bash -e

mkdir -p ../devreseek_search
cd ../devreseek_search

reseek=$src/reseek/bin/reseek

rm -f ../reseek_db/scop40.bca
rm -f *devreseek*

/bin/time -v -o devreseek.createdb.time \
	$reseek \
	  -convert ../reseek_db/scop40.cal \
	  -bca ../reseek_db/scop40.bca \
	  -log devreseek.createdb.log

/bin/time -v -o devreseek.time \
	$reseek \
	  -search ../reseek_db/scop40.bca \
	  -db ../reseek_db/scop40.bca \
	  -evalue 10 \
	  -output devreseek.tsv \
	  -log devreseek.search.log

/bin/time -v -o devreseek-sensitive.time \
	$reseek \
	  -search ../reseek_db/scop40.bca \
	  -db ../reseek_db/scop40.bca \
	  -sensitive \
	  -evalue 10 \
	  -output devreseek-sensitive.tsv \
	  -log devreseek-sensitive.search.log
