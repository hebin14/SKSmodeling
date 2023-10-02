#!/bin/bash

if [ $# -lt 2 ]; then
    echo 'datadir and target dir requlired'
    exit 1
fi

datadir=$1
target=$2
mkdir -p $target
rm $target/*
params_all=(vpvsrho vpvhvsvhrhogcgs) #models

nprocs=`grep ^NPROC DATA/Par_file | grep -v -E '^[[:space:]]*#' | cut -d = -f 2`
for param in ${params_all[@]};do
  for iproc in `seq 0 $((nprocs-1))`;do
    filein=`echo $param $iproc $datadir | awk '{printf"%s/proc%06d_%s.bin\n",$3,$2,$1}'`
    cp $filein $target/
  done
done
