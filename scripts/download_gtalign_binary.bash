#!/bin/bash -e

if [ -s ../bin/gtalign ] ; then
	echo "gtalign downloaded"
	exit 0
fi

mkdir -p ../gtalign_v0.15.0
cd ../gtalign_v0.15.0
wget https://github.com/minmarg/gtalign_alpha/archive/refs/tags/v0.15.0-alpha.tar.gz
tar -xvf v0.15.0-alpha.tar.gz gtalign_alpha-0.15.0-alpha/Linux_installer_mp/bin/gtalign
cp -v gtalign_alpha-0.15.0-alpha/Linux_installer_mp/bin/gtalign ../bin

chmod +x ../bin/gtalign