#!/bin/bash -e

if [ -f ../scop40pdb/pdb/d8abpa_ ] ; then
	echo "PDB files downloaded"
	exit 0
fi

mkdir -p ../scop40pdb
cd ../scop40pdb
wget https://wwwuser.gwdg.de/~compbiol/foldseek/scop40pdb.tar.gz
tar -zxf scop40pdb.tar.gz
echo "PDB files extracted"
