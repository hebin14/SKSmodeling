#!/bin/bash
data_dir=./smooth_init
target_dir=./initial_model
for fbin in `ls ${data_dir}/*_smooth.bin`;do
  	prefix=`echo ${fbin##*/}`
    tmp_proc=`echo $prefix |awk '{split($0,a,"_"); print a[1]}'` 
    tmp_mdnm=`echo $prefix |awk '{split($0,a,"_"); print a[2]}'` 
    echo $fbin $tmp_proc $tmp_mdnm
    cp ${data_dir}/${tmp_proc}_${tmp_mdnm}_smooth.bin $target_dir/${tmp_proc}_${tmp_mdnm}.bin
done
