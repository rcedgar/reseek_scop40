#!/bin/bash -e

if [ -d ../gtalign_output ] ; then
	echo "Use existing ../gtalign_output"
	exit 0
fi

mkdir ../gtalign_output

/bin/time -v -o ../gtalign_output/gtalign.time \
	../bin/gtalign \
	  --qrs=../scop40pdb/pdb/ \
	  --rfs=../scop40pdb/pdb/ \
	  -s 0 \
	  -o ../gtalign_output/
