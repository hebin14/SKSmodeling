#!/bin/bash
#SBATCH --ntasks=40
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --job-name sks_tomo
#SBATCH --output=out.log
#SBATCH --partition debug


currentdir=`pwd`

cd $SLURM_SUMBIT_DIR

cd $currentdir
mkdir -p OUTPUT_FILES 
mkdir -p OUTPUT_FILES/DATABASES_MPI
echo "running example: `date`"
# sets up directory structure in current example directory
echo $currentdir
#MYSEM3D=/home1/08807/binhe/scratch/AZaniFWI3/specfem3d
MYSEM3D=../specfem3d
#module load intel/18.0.2.199  mvapich2/2.3.1 
#ml intel impi
ml intel openmpi

# stores setup
cp DATA/meshfem3D_files/Mesh_Par_file OUTPUT_FILES/
cp DATA/Par_file OUTPUT_FILES/
cp DATA/FORCESOLUTION OUTPUT_FILES/
cp DATA/STATIONS OUTPUT_FILES/

# get the number of processors, ignoring comments in the Par_file
NPROC=`grep ^NPROC DATA/Par_file | grep -v -E '^[[:space:]]*#' | cut -d = -f 2`

BASEMPIDIR=`grep ^LOCAL_PATH DATA/Par_file | cut -d = -f 2 `
mkdir -p $BASEMPIDIR

# runs in-house mesher
if [ "$NPROC" -eq 1 ]; then
  # This is a serial simulation
  echo
  echo "  running mesher..."
  echo
  $MYSEM3D/bin/xmeshfem3D
else
  # This is a MPI simulation
  echo
  echo "  running mesher on $NPROC processors..."
  echo
  mpirun -np $NPROC $MYSEM3D/bin/xmeshfem3D
fi
# checks exit code
if [[ $? -ne 0 ]]; then exit 1; fi

# runs database generation
if [ "$NPROC" -eq 1 ]; then
  # This is a serial simulation
  echo
  echo "  running database generation..."
  echo
  ./bin/xgenerate_databases
else
  # This is a MPI simulation
  echo
  echo "  running database generation on $NPROC processors..."
  echo
  mpirun -np $NPROC $MYSEM3D/bin/xgenerate_databases
fi

# checks exit code
if [[ $? -ne 0 ]]; then exit 1; fi
# runs simulation
if [ "$NPROC" -eq 1 ]; then
  # This is a serial simulation
  echo
  echo "  running solver..."
  echo
  $MYSEM3D/bin/xspecfem3D
else
  # This is a MPI simulation
  echo
  echo "  running solver on $NPROC processors..."
  echo
  mpirun -np $NPROC $MYSEM3D/bin/xspecfem3D
fi

echo
echo "see results in directory: OUTPUT_FILES/"
echo
echo "done"
rm shot*
echo `date`
