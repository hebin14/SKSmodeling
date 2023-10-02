#!/bin/bash

gmt gmtset BASEMAP_TYPE plain
gmt gmtset MEASURE_UNIT cm
gmt gmtset ANNOT_FONT_SIZE_PRIMARY 12p LABEL_FONT_SIZE 12p ANNOT_FONT_SIZE_SECONDARY 12p
gmt gmtset LABEL_FONT Helvetica ANNOT_FONT_PRIMARY Helvetica ANNOT_FONT_SECONDARY Helvetica 
gmt gmtset LABEL_OFFSET 0.1c
gmt gmtset COLOR_BACKGROUND 28/48/104
gmt gmtset COLOR_FOREGROUND white

lonmin=140.0
lonmax=142.0
latmin=38.75
latmax=40.75
RMAP=$lonmin/$lonmax/$latmin/$latmax

cat topo_japan.dat | awk '{print $1,$2,$3*0.001}' | gmt blockmedian -R$RMAP -I0.02 | gmt surface -R$RMAP -I0.02 -Gtopo.grd -T0.25
scale=1.0
vmin=`gmt grdinfo topo.grd |grep v_min | awk '{print $3*a}' a=$scale`
vmax=`gmt grdinfo topo.grd |grep v_min | awk '{print $5*a}' a=$scale`
echo 'topo min/max:' $vmin $vmax
vmin=-2
vmax=2
gmt makecpt -Cvik -T$vmin/$vmax/100+n  > topo.cpt
xwidth=8
ywidth=6
xwidth_small=2
ywidth_small=2
p1="140 38.75"
p2="140 40.75"
p3="142 40.75"
p4="142 38.75"
gmt begin topo jpg
    
    gmt basemap  -R$RMAP -JX${xwidth}c/${ywidth}c  -Bxa$xtick+l"Lon (deg)" -By${ytick}+l"Lat (deg)" -BWeSN
    gmt grdimage topo.grd -Ctopo.cpt  -E200
    gmt colorbar -Ctopo.cpt -Bxa1.0+l"topography (km)" -DjMR+w2c/0.3c+o-1c/0c+m+e+v
    cp station.dat source.dat
    nstat=`cat station.dat |wc -l`
    for isour in `seq 2 $nstat`;do
        evtfile=`cat source.dat |sed -n "${isour}p"` # loop over all virtual evts
        elon=`echo $evtfile |awk '{print $3}'`
        elat=`echo $evtfile |awk '{print $2}'`
        echo $elon $elat | gmt psxy -St0.2c -Gblack
    done
    gmt inset begin -DjBR+w${xwidth_small}c/${ywidth_small}c+o0.05c/0.05c -F+gwhite
        gmt coast -JM? -R135/145/35/42 -W1p -N3 -Bwesn --MAP_FRAME_TYPE=plain 
        echo $p1 $p2 | gmt plot -A -W1p,red << EOF
        $p1
        $p2
EOF
        echo $p2 $p3 | gmt plot -A -W1p,red << EOF
        $p2
        $p3
EOF
        echo $p3 $p4 | gmt plot -A -W1p,red << EOF
        $p3
        $p4
EOF
        echo $p4 $p1 | gmt plot -A -W1p,red << EOF
        $p4
        $p1
EOF
    gmt inset end
gmt end 


rm *.cpt

