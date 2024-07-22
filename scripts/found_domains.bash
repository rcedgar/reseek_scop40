#!/bin/bash -e

mkdir -p ../out
cd ../out

ls /c/data/scop40pdb/pdb \
  > scop40pdb_pdb.domids

cut -f1 /c/a/res/scop/data_1.75/dir.cla.scop.txt_1.75 \
  | grep -v "^#" \
  > scop.domids

sort scop40pdb_pdb.domids scop.domids scop.domids \
  | uniq -u \
  > scop40pdb_pdb_not_in_scop.domids

sort scop40pdb_pdb.domids scop.domids \
  | uniq -d \
  > scop40pdb_pdb_in_scop.domids

fgrep -wFf scop40pdb_pdb_in_scop.domids $res/scop/data_1.75/dir.cla.scop.txt_1.75 \
  | cut -f1,4 \
  > domain_family.tsv
