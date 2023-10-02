#/bin/bash

FC="mpif90 -std08 -traceback -warn all"
cd src 
set -e -x

iso=aziso
$FC -g -c utm_geo.f90 -o utm_geo.o -O3 
$FC -g -c ${iso}_read_media3D_mpi.f90 -o ${iso}_read_media3D.o -O3 
$FC -g -c ${iso}_read_media3D_delta_mpi.f90 -o ${iso}_read_media3D_delta.o -O3 
$FC ${iso}_read_media3D.o utm_geo.o -o ../bin/${iso}_read_media 
$FC ${iso}_read_media3D_delta.o utm_geo.o -o ../bin/${iso}_read_media_delta 

$FC -g -c read_media3D_mpi.f90 -o read_media3D.o -O3 
$FC -g -c read_media3D_delta_mpi.f90 -o read_media3D_delta.o -O3 
$FC read_media3D.o utm_geo.o -o ../bin/read_media 
$FC read_media3D_delta.o utm_geo.o -o ../bin/read_media_delta 
rm *.o 
cd ..
