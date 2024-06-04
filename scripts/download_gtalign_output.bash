#!/bin/bash -e

if [ -d ../gtalign_output ] ; then
	echo "Found ../gtalign_output"
	exit 0
fi

mkdir -p ../gtalign_output
cd ../gtalign_output

wget 'https://zenodo.org/records/11148018/files/gtalign-benchmark-data.tgz?download=1'
tar -zxf gtalign-benchmark-data.tgz
