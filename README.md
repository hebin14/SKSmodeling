# SKSmodeling
A work-flow for SKS modeling using FK-SEM injection

# SPECFEM3D
Some modifications have been done with specfem3D, e.g, adding parameters like AZIMUTHAL_ANISOTROPY in Par_file, modifying several files in src/generate_databases to read C21 tomography files and saving the corresponding binary files; modifying src/couple_with_injection.f90 as suggested by Kai.
By running myinstall.sh in specfem3d, you could remake everything and reinstall specfem.

# How to run these examples step by step
1. Preparations
   install specfem3D
   make sactools_c in order to plot the data later
2. run mesh_ak135
   go to mesh_ak135 folder
   in ../model/ak135, modify and run creat_ansi_C21.py to design your azimuthal anisotropy parameters, like strength and fast azimuthal angle
   it will generate a file "tomography_ak135_C21_angle...."
   copy ../model/tomography_ak135_C21_angle.... to DATA/tomo_files/tomography_model.xyz
   submit a job for simulation, sbatch sbash_tomo.sh
   check out.log to see if it runs normally
   The output seismograms will be stored in OUTPUT_FILES and the binary velocity models will be stored in OUTPUT_FILES/DATABASES_MPI

