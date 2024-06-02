#!/bin/bash -e

outdir=/c/int/scop40pdb/alignResults_with_family
mkdir -p $outdir

# Sort by increasing E-value, FPs before TPs
for mode in veryfast fast sensitive verysensitive
do
	algo=reseek_$mode
	echo === $algo ===
	./alignResults_with_family.py $algo \
	  | sort -k3,3g -k4 \
	  > $outdir/$algo.tsv
done

# Sort by increasing E-value, FPs before TPs
for algo in blastp newfoldseek foldseek
do
	echo === $algo ===
	./alignResults_with_family.py $algo \
	  | sort -k3,3g -k4 \
	  > $outdir/$algo.tsv
done

# Sort by decreasing score, FPs before TPs
for algo in dali tm
do
	echo === $algo ===
	./alignResults_with_family.py $algo \
	  | sort -k3,3rg -k4 \
	  > $outdir/$algo.tsv
done
