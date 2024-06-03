#!/bin/bash -e

mkdir -p ../results
cd ../results

fns=" \
	../blastp_search/blastp_search.time \
	../foldseek_db/foldseek_createdb.time \
	../foldseek_search/foldseek_search.time \
	../reseek_db/reseek_pdb2cal.time \
	../reseek_search/fast.time \
	../reseek_search/sensitive.time \
	../reseek_search/veryfast.time \
	../reseek_search/verysensitive.time"

echo "time	mem	method" > elapsed_time_and_memory.tsv
for fn in $fns
do
	time=`grep -h "Elapsed (wall clock) time" $fn | sed "-es/.* //"`
	mem=`grep -h "Maximum resident set" $fn | sed "-es/.* //"`
	name=`echo $fn | sed "-es/reseek_search\//reseek-/" | sed "-es/.*\///" | sed "-es/\.time//"`
	echo "$time	$mem	$name"
done | tee -a elapsed_time_and_memory.tsv
