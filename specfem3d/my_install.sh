#ganymede
#./configure CC=icc FC=ifort MPIFC=mpifort MPI_INC=/opt/ohpc/pub/mpi/mvapich2-intel/2.3.1/include --with-mpi
#nia
ml intel openmpi
./configure CC=icc FC=ifort MPIFC=mpifort --with-mpi