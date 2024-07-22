#!/bin/bash -e

foldseek=/c/sw/foldseek/newfoldseek

query_pdbdir=/c/data/scop40pdb/pdb
db=/c/int/scop40/foldseek_db_scop40/scop40
tsvdir=/c/int/scop40pdb/foldseek_output
tmpdir=/c/int/scop40/newfoldseek_tmp
rm -rf $tmpdir
mkdir -p $tsvdir
cd $tsvdir

mkdir -p ../time

date "+%D %H:%M:%S" > ../time/newfoldseek_searchc.date

/bin/time -v -o ../time/newfoldseek_searchc.time \
$foldseek \
  easy-search \
  $query_pdbdir \
  $db \
  -s 9.5 --max-seqs 2000 -e 10 \
  --format-output "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,cigar" \
  newfoldseekc.tsv \
  $tmpdir

date "+%D %H:%M:%S" >> ../time/newfoldseek_searchc.date
