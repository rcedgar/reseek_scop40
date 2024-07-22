#!/bin/bash -e

./download_foldseek_binary.bash

query_pdbdir=../scop40pdb/pdb
db=../foldseek_db/scop40

tmpdir=../foldseek_tmp
rm -rf $tmpdir

mkdir -p ../foldseek_search
cd ../foldseek_search

/bin/time -v -o foldseek_search.time \
	../bin/foldseek \
	  easy-search \
	  $query_pdbdir \
	  $db \
	  -s 9.5 --max-seqs 2000 -e 10 \
	  foldseek.tsv \
	  $tmpdir
