#!/bin/bash
#SBATCH --partition=debug
#SBATCH --ntasks=40
#SBATCH --nodes=1
#SBATCH --time=00:59:59
#SBATCH --output=out.log
set -e 
ml intel openmpi
source activate pygmt
mkdir -p grdfolder

path=../../OUTPUT_FILES/DATABASES_MPI
#script from Nanqiao and Ting
#modified by Bin 2022-04-15
pwd
NPROC=`grep ^NPROC ../DATA/Par_file | grep -v -E '^[[:space:]]*#' | cut -d = -f 2`

z0=-300.  #starting depth
z1=0.     #ending depth
dist=5    #distance along profile for gmt track
nz=101


##===============================================##
##        get profile coordinate                 ##
##===============================================##
name1=A
name2=B
##first profile##
line=`cat ./model/profiles/profiles.lonlat |sed -n "1p"`
lon0=`echo $line |awk '{print $1}'`
lat0=`echo $line |awk '{print $2}'`
lon1=`echo $line |awk '{print $3}'`
lat1=`echo $line |awk '{print $4}'`
echo "$name1 $lon0/$lat0 $name1 $lon1/$lat1"
gmt project -C$lon0/$lat0 -E$lon1/$lat1 -G$dist -Q > input/prof$name1.tmp

##second profile##
line=`cat ./model/profiles/profiles.lonlat |sed -n "2p"`
lon0=`echo $line |awk '{print $1}'`
lat0=`echo $line |awk '{print $2}'`
lon1=`echo $line |awk '{print $3}'`
lat1=`echo $line |awk '{print $4}'`
echo "$name2 $lon0/$lat0 $name2 $lon1/$lat1"
gmt project -C$lon0/$lat0 -E$lon1/$lat1 -G$dist -Q > input/prof$name2.tmp

:>input/prof$name1.cords
:>input/prof$name2.cords
for ((i=0;i<$nz;i++));
do
    dep=`printf %g $(echo "scale=4; 1000*($z0 + ($z1 - $z0) / ($nz-1) * $i)"|bc)`
    awk -v a=$dep '{print $1,$2,a,$3}' input/prof$name1.tmp >> input/prof$name1.cords
    awk -v a=$dep '{print $1,$2,a,$3}' input/prof$name2.tmp >> input/prof$name2.cords
done
rm input/prof$name1.tmp input/prof$name2.tmp



declare -A bounds1
declare -A bounds2
info1=`gmt gmtinfo -C input/prof$name1.cords`
info2=`gmt gmtinfo -C input/prof$name2.cords`
echo 'coordinate info1::'$info1
echo 'coordinate info2::'$info2

dmin1=`echo $info1 | awk '{print $1}'`
dmax1=`echo $info1 | awk '{print $2}'`
dmin2=`echo $info2 | awk '{print $1}'`
dmax2=`echo $info2 | awk '{print $2}'`

bounds1=-R$dmin1/$dmax1/0.1/200
bounds2=-R$dmin2/$dmax2/0.1/200

echo 'bound1: '$bounds1
echo 'bound2: '$bounds2

#===============================================##
#  get data on coor and transfom into grd       ##
#===============================================##

echo '========generating grd files==============='
iso=aziso
kind=true
mod=M00
file1=prof$name1.$kind.$mod
file2=prof$name2.$kind.$mod
path=../OUTPUT_FILES/DATABASES_MPI
mpirun -np $NPROC ./bin/${iso}_read_media \
    ../OUTPUT_FILES/DATABASES_MPI  ${path} \
    input/prof$name1.cords ./input/$file1
    
mpirun -np $NPROC ./bin/${iso}_read_media \
    ../OUTPUT_FILES/DATABASES_MPI  ${path} \
    input/prof$name2.cords ./input/$file2


