#!/bin/bash -e

if [ -s ../reseek_db/scop40.cal ] ; then
	echo "scop40.cal found"
	exit 0
fi

./download_reseek_binary.bash
./download_scop40pdb.bash

mkdir -p ../reseek_db
cd ../reseek_db

find ../scop40pdb/pdb \
  | grep -v "/pdb$" \
  > pdb.files

/bin/time -v -o reseek_pdb2cal.time \
	reseek \
	  -pdb2cal pdb.files \
	  -output scop40.cal

# Remove chain identifier from label to be consistent
#  with scop40pdb/alignResults/ in Foldseek supp. data
sed -i -es/"_.$//" scop40.cal
