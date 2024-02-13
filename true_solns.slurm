#! /bin/bash

#SBATCH --mem=200g
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=cpu
#SBATCH --array=2-40
#SBATCH --account=bbxw-delta-cpu
#SBATCH -t 20:00:00
#SBATCH --constraint="scratch"
#SBATCH -o true-solns-%j-%a.out
#SBATCH --mail-user=alee@stac.edu
#SBATCH --mail-type=ALL


###GPU options ###

##Old hello options ###
##SBATCH -j hello
##SBATCH -p normal
##SBATCH -c 1 #one CPU core
##SBATCH -t 10:00
##SBATCH -o hello-%j.out
##SBATCH --mail-type=ALL
##SBATCH --mail-user=alee@stac.edu

##module reset
module load anaconda3_cpu
module list
echo "job is starting on `hostname`"
srun python3 true_solns.py $SLURM_ARRAY_TASK_ID
echo "job finished"
