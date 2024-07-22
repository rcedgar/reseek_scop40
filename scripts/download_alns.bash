#!/bin/bash -e

if [ -s ../alns/foldseek.txt ] ; then
	echo "Alns downloaded "
	exit 0
fi

mkdir -p ../alns
cd ../alns
wget https://wwwuser.gwdg.de/~compbiol/foldseek/scop.benchmark.result.tar.gz
tar -zxf scop.benchmark.result.tar.gz
ls -lh ../alns
echo "Alns extracted"
