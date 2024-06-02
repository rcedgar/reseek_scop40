#!/bin/bash -e

if [ -s ../bin/reseek ] ; then
	echo "Reseek binary found"
	exit 0
fi

mkdir -p ../bin
cd ../bin

wget \
  -O reseek \
  https://github.com/rcedgar/reseek/releases/download/v1.2-beta/reseek_linux_1.2-beta

chmod +x reseek
ls -lh ../bin/reseek
