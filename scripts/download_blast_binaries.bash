#!/bin/bash -e

mkdir -p ../blast_binaries
cd ../blast_binaries

if [ -s ../bin/makeblastdb ] ; then
	echo "BLAST binaries downloaded"
	exit 0
fi

wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.15.0+-x64-linux.tar.gz
tar -zxf ncbi-blast-2.15.0+-x64-linux.tar.gz

mkdir -p ../bin
cd ../bin

cp -v ../blast_binaries/ncbi-blast-2.15.0+/bin/blastp .
cp -v ../blast_binaries/ncbi-blast-2.15.0+/bin/makeblastdb .

echo "BLAST binaries extracted"
