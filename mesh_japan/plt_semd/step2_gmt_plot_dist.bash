#shell for plotting
export SAC_DISPLAY_COPYRIGHT=0
gmt set BASEMAP_TYPE plain
gmt set MEASURE_UNIT cm
gmt set ANNOT_FONT_SIZE_PRIMARY 12p LABEL_FONT_SIZE 12p ANNOT_FONT_SIZE_SECONDARY 12p
gmt set LABEL_FONT Helvetica ANNOT_FONT_PRIMARY Helvetica ANNOT_FONT_SECONDARY Helvetica 
gmt set LABEL_OFFSET 0.1c
gmt set COLOR_BACKGROUND 28/48/104
gmt set COLOR_FOREGROUND white
gmt set FORMAT_GEO_MAP=+D
#!/bin/bash
path=$1
band=T005_T020

lp=`echo $band |awk '{printf"%d",substr($1,2,3)}'`
hp=`echo $band |awk '{printf"%d",substr($1,7,3)}'`
lf=`echo $hp | awk '{print 1.0/$1}'`
hf=`echo $lp | awk '{print 1.0/$1}'`
ls $path/*.BXZ.semd.sac >dummy.lst
nstats=`cat dummy.lst | wc -l`
:>split_intensity.lst
for ist in `seq $nstats`;do
    zfile=`sed "${ist}q;d" dummy.lst`
    rfile=${zfile/BXZ/BXR}
    tfile=${zfile/BXZ/BXT}
    sac<<EOF
        r $zfile $rfile $tfile
        taper;bp co $lf $hf n 4 p 2; w $zfile.$band $rfile.$band $tfile.$band;q
EOF
    ~/software/sactools_c/get_spliting_intensity $tfile.$band $rfile.$band 50 150 >>split_intensity.lst
done

ls $path/*.BXZ.semd.sac.$band >bxz.lst
ls $path/*.BXR.semd.sac.$band >bxr.lst
ls $path/*.BXT.semd.sac.$band >bxt.lst
ampnorm=0.0
for ist in `seq $nstats`;do
    rfile=`sed "${ist}q;d" bxr.lst`
    depmax=`~/software/sactools_c/lsacmax 0 200 $rfile`
    ampnorm=`echo $ampnorm $depmax $nstats |awk '{print $1+$2/$3}'`
done
saclst dist f $path/*.BXZ.semd.sac.$band | awk '{print $2}'>dist.lst

gmtinfo=`gmt gmtinfo -C dist.lst`
distmin=`echo $gmtinfo | awk '{print $1-10}'`
distmax=`echo $gmtinfo | awk '{print $2+10}'`
ampnorm=`echo $ampnorm | awk '{print 2.0/$1}'`
tbeg=0
tend=200
echo 'time range from file::'$tbeg,$tend,'with data rescaled by:'$ampnorm
sc=$ampnorm/0
:>stnm.lst
i=0
while read line; do
  dummy=`echo $line |awk -F/ '{print $2}'`
  stnm=`echo $dummy |awk -F. '{print $1"."$2}'`
  echo $tbeg $i $stnm >> stnm.lst
    (( i++ ))
done <bxz.lst

xwidth=8.0
ywidth=16.0
out=$path.zrt
gmt begin $out jpg
    gmt subplot begin 1x3 -Fs${xwidth}c/${ywidth}c
    gmt subplot set
    gmt basemap -R-4/4/0/360 -Bx+l"Splitting time (s)" -By+l"Baz (deg)" -Bafg 
    cat split_intensity.lst | awk '{print $3,$2}' | gmt plot -Sc0.5c

    gmt subplot set
    gmt psbasemap -R$tbeg/$tend/$distmin/$distmax -Bx+l'time(s)'  -BweSn+t'R comp'
    cat bxr.lst | gmt pssac -Ek -M$sc -W0.5p

    gmt subplot set
    gmt psbasemap -R$tbeg/$tend/$distmin/$distmax -Bx+l'time(s)' -By+l'Distance (km)' -BwESn+t'T comp'
    cat bxt.lst | gmt pssac -Ek -M$sc -W0.5p
    gmt subplot end
gmt end

# rm *.lst
