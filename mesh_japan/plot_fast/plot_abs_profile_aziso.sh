#!/bin/bash
gmt set BASEMAP_TYPE plain
gmt set MEASURE_UNIT cm
gmt set ANNOT_FONT_SIZE_PRIMARY 8p LABEL_FONT_SIZE 8p ANNOT_FONT_SIZE_SECONDARY 6p
gmt set LABEL_FONT Helvetica ANNOT_FONT_PRIMARY Helvetica ANNOT_FONT_SECONDARY Helvetica 
gmt set LABEL_OFFSET 0.1c
gmt set COLOR_BACKGROUND 28/48/104
gmt set COLOR_FOREGROUND white
set -e 
mkdir -p grdfolder pics

name1=A
name2=B
kind=true
imodel=00
mod=M$imodel

profs=(dummy A B)
declare -A bounds1
declare -A bounds2
info1=`gmt gmtinfo -C input/prof$name1.cords`
info2=`gmt gmtinfo -C input/prof$name2.cords`
echo 'coordinate info1::'$info1
echo 'coordinate info2::'$info2

dmin1=`echo $info1 | awk '{print $1}'`
dmax1=`echo $info1 | awk '{print $2}'`
dmin2=`echo $info2 | awk '{print $3}'`
dmax2=`echo $info2 | awk '{print $4}'`

dminz=`echo $info1 | awk '{print -$6*0.001}'`
dmaxz=`echo $info1 | awk '{print -$5*0.001}'`
echo $dminz $dmaxz
bounds1=-R$dmin1/$dmax1/$dminz/$dmaxz
bounds2=-R$dmin2/$dmax2/$dminz/$dmaxz

echo 'bound1: '$bounds1
echo 'bound2: '$bounds2
nxx=128
nzz=128

    
file1=prof$name1.$kind.$mod
file2=prof$name2.$kind.$mod
cat input/prof$name1.cords | awk '{print $1, -$3*0.001}' >xz.dat
paste xz.dat input/$file1 >$file1
cat input/prof$name2.cords | awk '{print $2, -$3*0.001}' >yz.dat
paste yz.dat input/$file2 >$file2

dzz=`echo $nzz $dminz $dmaxz |awk '{print ($3-$2)/($1-1)}'`
dxx=`echo $nxx $dmin1 $dmax1 |awk '{print ($3-$2)/($1-1)}'`

cat $file1 | awk '{print $1, $2, $3*0.001}' |gmt blockmedian -I$dxx/$dzz $bounds1|  gmt surface -Ggrdfolder/vpv.$file1.grd -I$dxx/$dzz -T1.0 ${bounds1}
cat $file1 | awk '{print $1, $2, $4*0.001}' |gmt blockmedian -I$dxx/$dzz $bounds1|  gmt surface -Ggrdfolder/vph.$file1.grd -I$dxx/$dzz -T1.0 ${bounds1}
cat $file1 | awk '{print $1, $2, $5*0.001}' |gmt blockmedian -I$dxx/$dzz $bounds1|  gmt surface -Ggrdfolder/vsv.$file1.grd -I$dxx/$dzz -T1.0 ${bounds1}
cat $file1 | awk '{print $1, $2, $6*0.001}' |gmt blockmedian -I$dxx/$dzz $bounds1|  gmt surface -Ggrdfolder/vsh.$file1.grd -I$dxx/$dzz -T1.0 ${bounds1}
cat $file1 | awk '{print $1, $2, $8*100}' |gmt blockmedian -I$dxx/$dzz $bounds1|  gmt surface -Ggrdfolder/gc.$file1.grd -I$dxx/$dzz -T1.0 ${bounds1}
cat $file1 | awk '{print $1, $2, $9*100}' |gmt blockmedian -I$dxx/$dzz $bounds1|  gmt surface -Ggrdfolder/gs.$file1.grd -I$dxx/$dzz -T1.0 ${bounds1}

dxx=`echo $nxx $dmin2 $dmax2 |awk '{print ($3-$2)/($1-1)}'`
cat $file2 | awk '{print $1,$2,$3*0.001}' |gmt blockmedian -I$dxx/$dzz $bounds2|  gmt surface -Ggrdfolder/vpv.$file2.grd -I$dxx/$dzz -T1.0 ${bounds2}
cat $file2 | awk '{print $1,$2,$4*0.001}' |gmt blockmedian -I$dxx/$dzz $bounds2|  gmt surface -Ggrdfolder/vph.$file2.grd -I$dxx/$dzz -T1.0 ${bounds2}
cat $file2 | awk '{print $1,$2,$5*0.001}' |gmt blockmedian -I$dxx/$dzz $bounds2|  gmt surface -Ggrdfolder/vsv.$file2.grd -I$dxx/$dzz -T1.0 ${bounds2}
cat $file2 | awk '{print $1,$2,$6*0.001}' |gmt blockmedian -I$dxx/$dzz $bounds2|  gmt surface -Ggrdfolder/vsh.$file2.grd -I$dxx/$dzz -T1.0 ${bounds2}
cat $file2 | awk '{print $1,$2,$8*100}' |gmt blockmedian -I$dxx/$dzz $bounds2|  gmt surface -Ggrdfolder/gc.$file2.grd -I$dxx/$dzz -T1.0 ${bounds2}
cat $file2 | awk '{print $1,$2,$9*100}' |gmt blockmedian -I$dxx/$dzz $bounds2|  gmt surface -Ggrdfolder/gs.$file2.grd -I$dxx/$dzz -T1.0 ${bounds2}

vmin=`gmt grdinfo grdfolder/vph.$file1.grd |grep v_min | awk '{print $3}'`
vmax=`gmt grdinfo grdfolder/vph.$file1.grd |grep v_min | awk '{print $5}'`
gmt makecpt -Cvik -T$vmin/$vmax/101+n -I -D > vp.cpt

vmin=`gmt grdinfo grdfolder/vsh.$file1.grd |grep v_min | awk '{print $3}'`
vmax=`gmt grdinfo grdfolder/vsh.$file1.grd |grep v_min | awk '{print $5}'`
gmt makecpt -Cvik -T$vmin/$vmax/101+n -I -D > vs.cpt

vmin=-10
vmax=10
gmt makecpt -Cvik -T$vmin/$vmax/101+n -I -D > gcgs.cpt

xwidth_model=4
ywidth_model=3

gmt begin $kind.$mod.prof$name1 jpg
    gmt subplot begin 2x3 -Fs${xwidth_model}c/${ywidth_model}c -M0.5c
    gmt subplot set # 1
    file=grdfolder/vpv.$file1.grd
    gmt basemap $bounds1 -JX${xwidth_model}c/-${ywidth_model}c -Bxa05f0.25+l"Longitude(deg)" -Bya40f20+l"Depth (km)" -BWesn+t'Vpv'
    gmt grdimage $file -Cvp.cpt  -E200
    gmt subplot set # 1
    file=grdfolder/vsv.$file1.grd
    gmt basemap $bounds1 -JX${xwidth_model}c/-${ywidth_model}c -Bxa05f0.25+l"Longitude(deg)" -Bya40f20+l"Depth (km)" -BWesn+t'Vsv'
    gmt grdimage $file -Cvs.cpt  -E200
    gmt subplot set # 1
    file=grdfolder/gc.$file1.grd
    gmt basemap $bounds1 -JX${xwidth_model}c/-${ywidth_model}c -Bxa05f0.25+l"Longitude(deg)" -Bya40f20+l"Depth (km)" -BWesn+t'Gc'
    gmt grdimage $file -Cgcgs.cpt  -E200


    gmt subplot set # 1
    file=grdfolder/vph.$file1.grd
    gmt basemap $bounds1 -JX${xwidth_model}c/-${ywidth_model}c -Bxa05f0.25+l"Longitude(deg)" -Bya40f20+l"Depth (km)" -BWeSn+t'Vph'
    gmt grdimage $file -Cvp.cpt  -E200
    gmt colorbar -Cvp.cpt -Bxa1.0 -By+l"(km/s)" -DjBC+w2c/0.3c+o0c/-1.5c+m+e+h
    gmt subplot set # 1
    file=grdfolder/vsh.$file1.grd
    gmt basemap $bounds1 -JX${xwidth_model}c/-${ywidth_model}c -Bxa05f0.25+l"Longitude(deg)" -Bya40f20+l"Depth (km)" -BWeSn+t'Vsh'
    gmt grdimage $file -Cvs.cpt  -E200
     gmt colorbar -Cvs.cpt -Bxa1.0 -By+l"(km/s)" -DjBC+w2c/0.3c+o0c/-1.5c+m+e+h
    gmt subplot set # 1
    file=grdfolder/gs.$file1.grd
    gmt basemap $bounds1 -JX${xwidth_model}c/-${ywidth_model}c -Bxa05f0.25+l"Longitude(deg)" -Bya40f20+l"Depth (km)" -BWeSn+t'Gs'
    gmt grdimage $file -Cgcgs.cpt  -E200
    gmt colorbar -Cgcgs.cpt -Bxa5.0 -By+l"(%)" -DjBC+w2c/0.3c+o0c/-1.5c+m+e+h

    gmt subplot end
gmt end


gmt begin $kind.$mod.prof$name2 jpg
    gmt subplot begin 2x3 -Fs${xwidth_model}c/${ywidth_model}c  -M0.5c
    gmt subplot set # 1
    file=grdfolder/vpv.$file2.grd
    gmt basemap $bounds2 -JX${xwidth_model}c/-${ywidth_model}c -Bxa05f0.25+l"Longitude(deg)" -Bya40f20+l"Depth (km)" -BWesn+t'Vpv'
    gmt grdimage $file -Cvp.cpt  -E200
    gmt subplot set # 1
    file=grdfolder/vsv.$file2.grd
    gmt basemap $bounds2 -JX${xwidth_model}c/-${ywidth_model}c -Bxa05f0.25+l"Longitude(deg)" -Bya40f20+l"Depth (km)" -BWesn+t'Vsv'
    gmt grdimage $file -Cvs.cpt  -E200
    
    gmt subplot set # 1
    file=grdfolder/gc.$file2.grd
    gmt basemap $bounds2 -JX${xwidth_model}c/-${ywidth_model}c -Bxa05f0.25+l"Longitude(deg)" -Bya40f20+l"Depth (km)" -BWesn+t'Gc'
    gmt grdimage $file -Cgcgs.cpt  -E200
    

    gmt subplot set # 1
    file=grdfolder/vph.$file2.grd
    gmt basemap $bounds2 -JX${xwidth_model}c/-${ywidth_model}c -Bxa05f0.25+l"Latitude(deg)" -Bya40f20+l"Depth (km)" -BWeSn+t'Vph'
    gmt grdimage $file -Cvp.cpt  -E200
    gmt colorbar -Cvp.cpt -Bxa1.0 -By+l"(km/s)" -DjBC+w2c/0.3c+o0c/-1.5c+m+e+h
    gmt subplot set # 1
    file=grdfolder/vsh.$file2.grd
    gmt basemap $bounds2 -JX${xwidth_model}c/-${ywidth_model}c -Bxa05f0.25+l"Latitude(deg)" -Bya40f20+l"Depth (km)" -BWeSn+t'Vsh'
    gmt grdimage $file -Cvs.cpt  -E200
    gmt colorbar -Cvs.cpt -Bxa0.5 -By+l"(km/s)" -DjBC+w2c/0.3c+o0c/-1.5c+m+e+h
    gmt subplot set # 1
    file=grdfolder/gs.$file2.grd
    gmt basemap $bounds2 -JX${xwidth_model}c/-${ywidth_model}c -Bxa05f0.25+l"Latitude(deg)" -Bya40f20+l"Depth (km)" -BWeSn+t'Gs'
    gmt grdimage $file -Cgcgs.cpt  -E200
    gmt colorbar -Cgcgs.cpt -Bxa5.0 -By+l"(%)" -DjBC+w2c/0.3c+o0c/-1.5c+m+e+h
    gmt subplot end
gmt end

rm xz.dat yz.dat
rm *.cpt
rm prof*
