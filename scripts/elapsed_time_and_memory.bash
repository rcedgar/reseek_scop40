#!/bin/bash

mkdir -p ../results
cd ../results

fns=" \
	../blastp_search/blastp_search.time \
	../foldseek_db/foldseek_createdb.time \
	../foldseek_search/foldseek_search.time \
	../reseek_db/reseek_pdb2cal.time \
	../devreseek_search/devfast.time \
	../devreseek_search/devsensitive.time \
	../devreseek_search/devveryfast.time"

echo "Time	Mem(kb)	Method" > elapsed_time_and_memory.tsv
for fn in $fns
do
	time=`grep -h "Elapsed (wall clock) time" $fn \
	  | sed "-es/.* //" \
	  | sed "-es/\..*//"`

	#        Maximum resident set size (kbytes): 327664
	mem=`grep -h "Maximum resident set" $fn \
	  | sed "-es/.*: //"`

	memkb=`python3 -c "print('%.1f' % ($mem/1024.0))"`

	name=`echo $fn \
	  | sed "-es/devreseek_search\//rsk-/" \
	  | sed "-es/reseek_search\//reseek-/" \
	  | sed "-es/.*\///" \
	  | sed "-es/\.time//"`
	echo "$time	$memkb	$name"
done >> elapsed_time_and_memory.tsv

ls -lh ../results/elapsed_time_and_memory.tsv
