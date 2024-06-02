#!/bin/bash -e

./download_blast_binaries.bash


mkdir -p ../blastp_search
cd ../blastp_search

/bin/time -v -o blastp_search.time \
	../bin/blastp \
	-query ../data/scop40.fa \
    -db ../blastdb/scop40 \
    -evalue 10 \
    -outfmt 6 \
    > blastp.tsv

