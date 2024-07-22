#!/bin/bash -e

mkdir -p ../blastdb
cd ../blastdb

makeblastdb -in ../data/scop40.fa -dbtype prot -out scop40
