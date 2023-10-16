ml gcc openmpi
./configure CC=gcc FC=gfortran MPIFC=mpif90 --with-mpi


##what I have changed (BinHe)
#1. Par_file add two variables, AZIMUTHAL_ANISOTROPY TRANSVERSE_ANISOTROPY
#   in order to do this, we need to add two parameters in src/shared/shared_par.F90 
#   then updating src/shared/read_parameter_file.F90 to read and bcast these two parameters from Par_file
#2. src/generate_databases/model_tomography.f90 search BinHe to see what I have modified

#3. src/generate_databases/get_model.f90 search BinHe to see how do I output some information for double check model parameters bebofre run solver

#4. src/generate_databases/save_array_solver.f90 modified inorder to save binary files for later check. If you think it is not necessary, do not modify it
