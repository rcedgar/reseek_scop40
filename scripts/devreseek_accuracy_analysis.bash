#!/bin/bash -e

mkdir -p ../accuracy_analysis
cd ../accuracy_analysis

rm -f *devreseek*

for mode in sf fold
do
	out=devreseek_$mode.txt
	sort -gk1 ../devreseek_search/devreseek.tsv \
	  | python3 ../scripts/accuracy_analysis.py 2 3 1 e $mode \
	  > $out
	if [ $mode == sf ] ; then
		grep -H ^SEPQ $out
	fi
done

for mode in sf fold
do
	out=devreseek-sensitive_$mode.txt
	sort -gk1 ../devreseek_search/devreseek-sensitive.tsv \
	  | python3 ../scripts/accuracy_analysis.py 2 3 1 e $mode \
	  > $out
	if [ $mode == sf ] ; then
		grep -H ^SEPQ $out
	fi
done
