#!/bin/bash

## get the plane wave injection parameters for sks waves
export SAC_DISPLAY_COPYRIGHT=0

phase=SKS
xmin=413103.390778675
xmax=584419.143939894
ymin=4289509.08496848
ymax=4511486.20594138
xx0=`echo $xmin $xmax |awk '{printf"%.2f",($1+$2)/2}'`
yy0=`echo $ymin $ymax |awk '{printf"%.2f",($1+$2)/2}'`

zz0=-400000.0
stlat=39.75
stlon=141                           # PARAMETERS TO BE SET BY USER
cdep=400.0  ## depth: km
tw=160.


fevt=fk_events_picked.lst
nevents=`cat $fevt |wc -l`
echo '..........' $nevents  events '..........'
for isour in `seq $nevents`;do
      evtfile=`cat $fevt |sed -n "${isour}p"` # loop over all virtual evts
      elon=`echo $evtfile |awk '{print $1}'`
      elat=`echo $evtfile |awk '{print $2}'`
      #=========================================================================
      dist=`~/software/sactools_c/distaz $stlat $stlon $elat $elon |awk '{print $1}' `
      baz=`~/software/sactools_c/distaz $stlat $stlon $elat $elon |awk '{print $2}' `
      az=`~/software/sactools_c/distaz $stlat $stlon $elat $elon  |awk '{print $3}' `
  
      ~/software/TauP-2.5.0/bin/taup_time -mod prem -h 0  -ph SKS -deg $dist >taup.out
      inc_ang=`cat taup.out |sed -n '6p' |awk '{print $7}'`  ## Incident angle
      cat >FKmodel_$phase${isour} <<EOF
#  input file for embedded FK modeiling
#
#  for each layer we give :
#  LAYER ilayer rho vp vs ztop
#  the last layer is the homogeneous half space
#
#
# model description  ---------------------
NLAYER             4
LAYER 1 2720.000 5800.000 3460.00 0.000
LAYER 2 3319.80 8040.000 4490.00 -50000.000
LAYER 3 3425.80 8300.000 4518.00 -150000.000
LAYER 4 3425.80 8300.000 4518.00 -200000.000
EOF
  cat >>FKmodel_$phase${isour} <<EOF
#----------------------------------------
# incident wave p or sv
INCIDENT_WAVE      sv
#----------------------------------------
# anlges of incomming wave
BACK_AZIMUTH               $baz
TAKE_OFF               $inc_ang
#----------------------------------------
FREQUENCY_MAX      0.5
#----------------------------------------
TIME_WINDOW       240
#----------------------------------------
# optionnal
 ORIGIN_WAVEFRONT  $xx0       $yy0      $zz0
# ORIGIN_TIME 
EOF
  cat >CMTSOLUTION_$phase${isour} <<eof
PDE  1999 01 01 00 00 00.00  $elon $elat -25000 4.2 4.2 hom_explosion
event name:       hom_explosion
time shift:       0.0000
half duration:    0.0
latorUTM:         $elat
longorUTM:        $elon
depth:            0
Mrr:       1.000000e+23
Mtt:       1.000000e+23
Mpp:       1.000000e+23
Mrt:       0.000000
Mrp:       0.000000
Mtp:       0.000000
eof
done