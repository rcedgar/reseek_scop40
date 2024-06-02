#!/bin/bash -e

if [ -s ../bin/foldseek ] ; then
	echo "Foldseek found"
	exit 0
fi

mkdir -p ../tmp
cd ../tmp

wget https://github.com/steineggerlab/foldseek/releases/download/8-ef4e960/foldseek-linux-avx2.tar.gz

tar -zxvf foldseek-linux-avx2.tar.gz

mkdir -p ../bin
cp -v ./foldseek/bin/foldseek ../bin

cd ../bin
rm -rf ../tmp

chmod +x ../bin/foldseek
ls -lh ../bin/foldseek
