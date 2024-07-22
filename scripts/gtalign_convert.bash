#!/bin/bash -e

cd ../gtalign_output

../scripts/gtalign_convert.py *.out \
  > gtalign.tsv
