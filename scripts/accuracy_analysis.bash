#!/bin/bash

outdir=/c/int/scop40pdb/accuracy_analysis
mkdir -p $outdir

indir=/c/int/scop40pdb/alignResults_with_family/

for mode in veryfast fast sensitive verysensitive
do
	algo=reseek_$mode
	echo === $algo ===
	./accuracy_analysis.py $indir/$algo.tsv e \
	  > $outdir/$algo.txt
done

for algo in dali tm
do
	echo === $algo ===
	./accuracy_analysis.py $indir/$algo.tsv s \
	  > $outdir/$algo.txt
done

for algo in foldseek newfoldseek blastp
do
	echo === $algo ===
	./accuracy_analysis.py $indir/$algo.tsv e \
	  > $outdir/$algo.txt
done
